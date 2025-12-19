from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class ProductModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    product_name: str
    concentration: str
    skin_type: List[str]
    key_ingredients: List[str]
    benefits: List[str]
    how_to_use: str
    side_effects: str
    price_inr: int
    schema_version: str = "1.0"


class QuestionItem(BaseModel):
    category: str
    question: str


class QuestionSet(BaseModel):
    count: int
    items: List[QuestionItem]


class TemplateSpec(BaseModel):
    name: str
    required_fields: List[str]
    logic_dependencies: List[str] = Field(default_factory=list)
    format_rules: Dict[str, Any] = Field(default_factory=dict)


class FAQItem(BaseModel):
    q: str
    a: str
    category: str
    source_field: Optional[str] = None


class FAQPage(BaseModel):
    template: str
    product: str
    supporting: Dict[str, Any]
    qa: List[FAQItem]


class ProductPage(BaseModel):
    template: str
    product: ProductModel
    blocks: Dict[str, Any]
    meta: Dict[str, Any]


class ComparisonPage(BaseModel):
    template: str
    product_a: str
    product_b: str
    comparison: Dict[str, Any]


class PipelineState(BaseModel):
    raw: Dict[str, Any]
    product_model: Optional[ProductModel] = None
    questions: Optional[QuestionSet] = None
    logic_ids: List[str] = Field(default_factory=list)
    template_specs: Dict[str, TemplateSpec] = Field(default_factory=dict)
    product_b: Optional[ProductModel] = None
    faq_page: Optional[FAQPage] = None
    product_page: Optional[ProductPage] = None
    comparison_page: Optional[ComparisonPage] = None
    documentation_md: Optional[str] = None
    error: Optional[str] = None
