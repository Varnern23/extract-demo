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
  @field_validator("section")
  @classmethod
  def validate_section(cls, v: Optional[str]) -> Optional[str]:
    if v is None:
      return v
    elif not re.fullmatch(r"[a-z]{1}", v.lower()):
      raise ValueError("section must be a single lowercase letter")
    return v
  @field_validator("number")
  @classmethod
  def validate_number(cls, v: str) -> str:
    if not (re.fullmatch(r"[0-9]{3}[Ll]{1}", v) or re.fullmatch(r"[0-9]{3}", v)):
      raise ValueError("class number must be 3 numbers and then nothing or the letter L")  
    return v
  @field_validator("title")
  @classmethod
  def validate_title(cls, v: str) -> str:
    """Title must be in title case"""
    if not v == str(v):
      raise ValueError("Title must be written in title case")
    return v
  @field_validator("credits")
  @classmethod
  def validate_credits(cls, v:float) -> float:
    if not v == float(v):
      raise ValueError("Credits must be in the form of a float")
    elif not (v >= 0 and v <= 4):
      raise ValueError("Credits must be between 0 and 4 inclusive")
    return v
  @field_validator("days")
  @classmethod
  def validate_days(cls, v:Optional[str]) -> Optional[str]:
    if not (v.lower() == "-m-w-f-" or  v.lower() == "--t-r--" or  v.lower() == "-mtw-f-" or v.lower() == "-m-wrf-" or v.lower() == "--t----" or v.lower() == "----r--" or v.lower() == "-------" or v.lower() == "-m-w---" or v == "" or v == None):
      raise ValueError("select an elidgible set of days")
    return v
  @field_validator("times")
  @classmethod
  def validate_times(cls, v:Optional[str]) -> Optional[str]:
    if v == None or v == "TBA":
      return v
    elif not re.fullmatch(r"[0-9]{1,2}[:]{1}[0-9]{2}[-]{1}[0-9]{1,2}[:]{1}[0-9]{2}[A,P]{1}[M]{1}", v) :
      raise ValueError("The given time slot is invalid it must be in the same format as 10:20-11:20AM")
    return v
  @field_validator("room")
  @classmethod
  def validate_room(cls, v:Optional[str]) -> Optional[str]:
    if v == None or v == "TBA" or v == "":
      return v
    elif not re.fullmatch(r"[A-Z]{4}\s?[0-9]{3}", v):
      raise ValueError("The given room is invalid")
    return v
  @field_validator("faculty")
  @classmethod
  def validate_faculty(cls, v:str) -> str:
    if v == str(v):
      return v
    elif not re.fullmatch(r"[A-Za-z]{1}[.]{1}\s?[A-Za-z'/\s]+| [A-Za-z'/\s]+", v):
      raise ValueError("Faculty name not inputted correctly please follow the guidline example: T. Allen")
    return v
  @field_validator("tags")
  @classmethod
  def validate_tags(cls, v:Optional[str]) -> Optional[str]:
    if not v or v.strip() == "":
      return v
    elif not re.fullmatch(r"[E][1-3]|[A, S, D, G, R]|[A, S, D, G, R][,]\s?[A, S, D, G, R]|[E][1-3][,]\s?[A, S, D, G, R]|[A, S, D, G, R][,]\s?[E][1-3]", v):
      raise ValueError("Tags not applied properly")
    return v 




  # Add other validators here as needed
