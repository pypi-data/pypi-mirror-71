from pathlib import Path
from typing import Optional, List

from pydantic import BaseModel


class Meta(BaseModel):
    title: str
    description: Optional[str] = None
    authors: List[str] = []
    date: Optional[str] = None
    hide_hierarchy: bool = False
    hide_title: bool = False


class Hierarchy(BaseModel):
    title: str
    link: str
    current: bool = False
    children: List['Hierarchy'] = []


class Page(BaseModel):
    meta: Meta
    content: str = ""
    excerpt: Optional[str] = None
    hierarchy: Optional['Hierarchy'] = None
    link: str = "#"


class Config(BaseModel):
    locale: str
    site_title: str
    copyright: Optional[str] = None
    content_dir: Path
