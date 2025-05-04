from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="manager")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship with TeamMember
    team_member = relationship("TeamMember", back_populates="user", uselist=False)


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    position = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    start_date = Column(Date)
    profile_picture_url = Column(String)
    public_notes = Column(Text)
    manager_notes = Column(Text)
    superior_id = Column(Integer, ForeignKey("team_members.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="team_member")
    superior = relationship("TeamMember", remote_side=[id], backref="direct_reports")
    
    # Other relationships
    objectives = relationship("Objective", back_populates="team_member", cascade="all, delete-orphan")
    meeting_logs = relationship("MeetingLog", foreign_keys="MeetingLog.team_member_id", back_populates="team_member", cascade="all, delete-orphan")
    managed_meetings = relationship("MeetingLog", foreign_keys="MeetingLog.manager_id", back_populates="manager")
    assigned_action_items = relationship("ActionItem", foreign_keys="ActionItem.assigned_to_member_id", back_populates="assigned_to")
    created_action_items = relationship("ActionItem", foreign_keys="ActionItem.assigned_by_manager_id", back_populates="assigned_by")


class Objective(Base):
    __tablename__ = "objectives"

    id = Column(Integer, primary_key=True, index=True)
    team_member_id = Column(Integer, ForeignKey("team_members.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="Active")
    start_period = Column(String)
    end_period = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    team_member = relationship("TeamMember", back_populates="objectives")
    key_results = relationship("KeyResult", back_populates="objective", cascade="all, delete-orphan")


class KeyResult(Base):
    __tablename__ = "key_results"

    id = Column(Integer, primary_key=True, index=True)
    objective_id = Column(Integer, ForeignKey("objectives.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    measurement_type = Column(String, nullable=False)
    target_value = Column(String)
    current_value = Column(String)
    start_date = Column(Date)
    deadline = Column(Date, nullable=False)
    complexity = Column(String)
    status = Column(String, default="Not Started")
    result_evaluation = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    objective = relationship("Objective", back_populates="key_results")


class MeetingLog(Base):
    __tablename__ = "meeting_logs"

    id = Column(Integer, primary_key=True, index=True)
    team_member_id = Column(Integer, ForeignKey("team_members.id"), nullable=False)
    manager_id = Column(Integer, ForeignKey("team_members.id"), nullable=False)
    meeting_date = Column(DateTime, nullable=False)
    notes = Column(Text)
    notes_structured = Column(Text)
    ai_summary = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    team_member = relationship("TeamMember", foreign_keys=[team_member_id], back_populates="meeting_logs")
    manager = relationship("TeamMember", foreign_keys=[manager_id], back_populates="managed_meetings")
    action_items = relationship("ActionItem", back_populates="meeting_log", cascade="all, delete-orphan")


class ActionItem(Base):
    __tablename__ = "action_items"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    assigned_to_member_id = Column(Integer, ForeignKey("team_members.id"), nullable=True)
    assigned_by_manager_id = Column(Integer, ForeignKey("team_members.id"), nullable=True)
    meeting_log_id = Column(Integer, ForeignKey("meeting_logs.id"), nullable=True)
    due_date = Column(Date)
    status = Column(String, default="To Do")
    priority = Column(String, default="Medium")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    assigned_to = relationship("TeamMember", foreign_keys=[assigned_to_member_id], back_populates="assigned_action_items")
    assigned_by = relationship("TeamMember", foreign_keys=[assigned_by_manager_id], back_populates="created_action_items")
    meeting_log = relationship("MeetingLog", back_populates="action_items")
