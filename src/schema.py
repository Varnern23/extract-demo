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
  def validate_number(cls, v: str) -> str:
    if not re.fullmatch(r"[1-9]{3}[L]{1}", v) or not re.fullmatch(r"[1-9]{3}", v):
      raise ValueError("class number must be 3 numbers and then nothing or the letter L")  
    return v
  def validate_title(cls, v: str) -> str:
    """Title must be in title case"""
    if not v.istitle():
      raise ValueError("Title must be written in title case")
    return v
  def validate_credits(cls, v:float) -> float:
    if not v == float(v):
      raise ValueError("Credits must be in the form of a float")
    elif not v >= 0 and not v <= 4:
      raise ValueError("Credits must be between 0 and 4 inclusive")
    return v
  def validate_days(cls, v:str) -> str:
    if not v.lower() == "-m-w-f-" or not v.lower() == "--t-th--" or not v.lower() == "-mtw-f-" or not v.lower() == "-m-wthf-" or not v.lower() == "-------" or not v == None:
      raise ValueError("select an elidgible set of days")
    return v
  def validate_times(cls, v:str) -> str:
    if not re.fullmatch(r"[0-9]{1,2}[:]{1}[0-9]{2}[-]{1}[0-9]{1,2}[:]{1}[0-9]{2}[A,P]{1}[M]{1}") or not v == None or not v == "TBA":
      raise ValueError("The given time slot is invalid it must be in the same format as 10:20-11:20AM")
    return v
  def validate_room(cls, v:str) -> str:
    if not re.fullmatch(r"[A-Z]{4}[1-4]{3}") or not v == "TBA" or not v == None:
      raise ValueError("The given room is invalid")
    return v
  def validate_faculty(cls, v:str) -> str:
    if not re.fullmatch(r"[A-Z]{1}[.]{1}[A-Za-z]+"):
      raise ValueError("Faculty name not inputted correctly please follow the guidline example: T. Allen")
    return v
  def validate_tags(cls, v:str) -> str:
    if not re.fullmatch(r"[E][1-3]|[A, S, D, G, R]|[A, S, D, G, R][,][A, S, D, G, R]|[E][1-3][,][A, S, D, G, R]") or not v == None:
      raise ValueError("Tags not applied properly")
    return v 




  # Add other validators here as needed
