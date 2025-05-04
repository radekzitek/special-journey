from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..dependencies import get_db, get_current_user, get_current_active_user

router = APIRouter(
    prefix="/team-members",
    tags=["team-members"],
    responses={404: {"description": "Not found"}}
)


@router.post("/", response_model=schemas.TeamMember)
def create_team_member(
    team_member: schemas.TeamMemberCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Create a new team member.
    
    Only users with admin role can create team members.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
        
    # Check if email already exists
    existing_member = crud.get_team_member_by_email(db, team_member.email)
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered for a team member"
        )
    
    return crud.create_team_member(db, team_member)


@router.get("/", response_model=List[schemas.TeamMember])
def read_team_members(
    skip: int = 0,
    limit: int = 100,
    superior_id: Optional[int] = None,
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get all team members.
    
    Admins can see all team members.
    Managers can see their direct reports.
    Filter by superior_id to get team members under a specific manager.
    """
    # If manager, only allow access to direct reports unless admin
    current_member = crud.get_team_member_by_user_id(db, current_user.id)
    
    if current_user.role != "admin":
        if not current_member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        # Override superior_id to only show direct reports for managers
        superior_id = current_member.id
    
    team_members = crud.get_team_members(db, skip=skip, limit=limit, superior_id=superior_id, include_inactive=include_inactive)
    return team_members


@router.get("/hierarchy", response_model=List[schemas.TeamMemberWithReports])
def read_team_members_hierarchy(
    superior_id: Optional[int] = None,
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get team members with their hierarchy (direct reports).
    
    Admins can see all hierarchies.
    Managers can only see their own hierarchy.
    """
    # If manager, only allow access to their own hierarchy unless admin
    current_member = crud.get_team_member_by_user_id(db, current_user.id)
    
    if current_user.role != "admin":
        if not current_member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        # Override superior_id to only show hierarchy under current manager
        if superior_id is not None and superior_id != current_member.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to view this hierarchy"
            )
        superior_id = current_member.id
    
    team_members = crud.get_team_members_with_hierarchy(db, superior_id=superior_id, include_inactive=include_inactive)
    return team_members


@router.get("/me", response_model=schemas.TeamMember)
def read_team_member_me(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get the current user's team member profile if it exists.
    """
    team_member = crud.get_team_member_by_user_id(db, current_user.id)
    if team_member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found for current user")
    return team_member


@router.get("/{team_member_id}", response_model=schemas.TeamMember)
def read_team_member(
    team_member_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get a specific team member by ID.
    
    Admins can see any team member.
    Managers can only see themselves and their direct reports.
    """
    team_member = crud.get_team_member(db, team_member_id)
    
    if team_member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found")
    
    # Check permissions
    if current_user.role != "admin":
        current_member = crud.get_team_member_by_user_id(db, current_user.id)
        if not current_member:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
            
        # Only allow access to self or direct reports
        is_self = team_member.user_id == current_user.id
        is_direct_report = team_member.superior_id == current_member.id
        
        if not (is_self or is_direct_report):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    return team_member


@router.put("/{team_member_id}", response_model=schemas.TeamMember)
def update_team_member(
    team_member_id: int,
    team_member: schemas.TeamMemberUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Update a team member.
    
    Admins can update any team member.
    Managers can only update their direct reports.
    """
    db_team_member = crud.get_team_member(db, team_member_id)
    
    if db_team_member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found")
    
    # Check permissions
    if current_user.role != "admin":
        current_member = crud.get_team_member_by_user_id(db, current_user.id)
        if not current_member:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        
        # Only allow updating direct reports
        if db_team_member.superior_id != current_member.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    # Check if email is being changed and already exists
    if team_member.email and team_member.email != db_team_member.email:
        existing = crud.get_team_member_by_email(db, team_member.email)
        if existing and existing.id != team_member_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered for another team member"
            )
    
    updated_team_member = crud.update_team_member(db, team_member_id, team_member)
    return updated_team_member


@router.delete("/{team_member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team_member(
    team_member_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Delete a team member.
    
    Only admins can delete team members.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    team_member = crud.get_team_member(db, team_member_id)
    if team_member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found")
    
    crud.delete_team_member(db, team_member_id)
    return