import os

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime


# ============================================================
# DATABASE CONNECTION
# ============================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///chat_history.db"
)


# PostgreSQL URLs sometimes start with postgres://.
# SQLAlchemy expects postgresql:// instead.

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql://",
        1
    )


# SQLite needs this setting.
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True
    )


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


Base = declarative_base()


# ============================================================
# CONVERSATION TABLE
# ============================================================

class Conversation(Base):

    __tablename__ = "conversations"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    title = Column(
        String(200),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.id"
    )


# ============================================================
# MESSAGE TABLE
# ============================================================

class Message(Base):

    __tablename__ = "messages"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    conversation_id = Column(
        Integer,
        ForeignKey(
            "conversations.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    role = Column(
        String(20),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    conversation = relationship(
        "Conversation",
        back_populates="messages"
    )

    sources = relationship(
        "Source",
        back_populates="message",
        cascade="all, delete-orphan",
        order_by="Source.id"
    )


# ============================================================
# SOURCE TABLE
# ============================================================

class Source(Base):

    __tablename__ = "sources"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    message_id = Column(
        Integer,
        ForeignKey(
            "messages.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    page = Column(
        String(50),
        nullable=False
    )

    passage = Column(
        Text,
        nullable=False
    )

    pdf_page = Column(
        String(50),
        nullable=False
    )

    pdf_url = Column(
        Text,
        nullable=False
    )

    message = relationship(
        "Message",
        back_populates="sources"
    )


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

Base.metadata.create_all(
    bind=engine
)


# ============================================================
# CREATE NEW CONVERSATION
# ============================================================

def create_conversation(title):

    db = SessionLocal()

    try:

        conversation = Conversation(
            title=title
        )

        db.add(conversation)

        db.commit()

        db.refresh(conversation)

        return conversation.id

    finally:

        db.close()


# ============================================================
# GET ALL CONVERSATIONS
# ============================================================

def get_conversations():

    db = SessionLocal()

    try:

        conversations = (
            db.query(Conversation)
            .order_by(
                Conversation.updated_at.desc()
            )
            .all()
        )

        return [
            {
                "id": conversation.id,
                "title": conversation.title,
                "created_at": conversation.created_at,
                "updated_at": conversation.updated_at
            }
            for conversation in conversations
        ]

    finally:

        db.close()


# ============================================================
# SAVE USER MESSAGE
# ============================================================

def save_user_message(
    conversation_id,
    content
):

    db = SessionLocal()

    try:

        message = Message(
            conversation_id=conversation_id,
            role="user",
            content=content
        )

        db.add(message)

        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id
            )
            .first()
        )

        if conversation:
            conversation.updated_at = datetime.utcnow()

        db.commit()

    finally:

        db.close()


# ============================================================
# SAVE ASSISTANT MESSAGE + SOURCES
# ============================================================

def save_assistant_message(
    conversation_id,
    content,
    sources
):

    db = SessionLocal()

    try:

        message = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=content
        )

        db.add(message)

        db.flush()

        for source in sources:

            db_source = Source(
                message_id=message.id,
                page=str(source["page"]),
                passage=source["passage"],
                pdf_page=str(source["pdf_page"]),
                pdf_url=source["pdf_url"]
            )

            db.add(db_source)

        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id
            )
            .first()
        )

        if conversation:
            conversation.updated_at = datetime.utcnow()

        db.commit()

    finally:

        db.close()


# ============================================================
# GET COMPLETE CONVERSATION
# ============================================================

def get_conversation(conversation_id):

    db = SessionLocal()

    try:

        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id
            )
            .first()
        )

        if not conversation:
            return None

        messages = []

        for message in conversation.messages:

            message_data = {
                "role": message.role,
                "content": message.content,
                "sources": []
            }

            for source in message.sources:

                message_data["sources"].append(
                    {
                        "page": source.page,
                        "passage": source.passage,
                        "pdf_page": source.pdf_page,
                        "pdf_url": source.pdf_url
                    }
                )

            messages.append(message_data)

        return {
            "id": conversation.id,
            "title": conversation.title,
            "messages": messages
        }

    finally:

        db.close()


# ============================================================
# DELETE CONVERSATION
# ============================================================

def delete_conversation(conversation_id):

    db = SessionLocal()

    try:

        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id
            )
            .first()
        )

        if conversation:

            db.delete(conversation)

            db.commit()

    finally:

        db.close()