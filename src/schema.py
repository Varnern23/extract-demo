"""
src/schema.py
--------------------------------
Defines the Pydantic schema for structured course data.

INSTRUCTIONS FOR STUDENTS:
  • This file defines the schema the model will use when returning structured JSON.
  • See the lab instructions for the full list of fields and constraints.
  • Add the missing fields (between 'program' and 'tags') and any validators
    needed to enforce the rules described in the lab.
  • Use None for optional or missing values.
"""

from pydantic import BaseModel, field_validator
from typing import Optional
import re

class SectionRow(BaseModel):
    program: str
    number: str
    section: Optional[str] = None
    title: str
    credits: float
    days: Optional[str] = None
    times: Optional[str] = None
    room: Optional[str] = None
    faculty: str
    # Add your other fields here (see README)
    tags: Optional[str] = None

    @field_validator("program")
    @classmethod
    def validate_program(cls, v: str) -> str:
        """Program must be three uppercase letters like CSC or MAT."""
        if not re.fullmatch(r"[A-Z]{3}", v):
            raise ValueError("program must be three uppercase letters")
        return v
    def validate_section(cls, v: str) -> str:
      if not re.fullmatch(r"[a-z]{1}", v):
        if not v == None:
          raise ValueError("section must be a single lowercase letter")
      return v

    def validate_title(cls, v: str) -> str:
       """Title must be in title case"""
      if istitle(v): False
            raise ValueError("program must be three uppercase letters")
      return v


    # Add other validators here as needed
