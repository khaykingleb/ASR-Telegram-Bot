variable "project_name" {
  type        = string
  description = "The name of the project."
  default     = ""
}

variable "environment" {
  type        = string
  description = "The environment type."
  default     = ""
}

variable "region" {
  type        = string
  description = "Servers location in Amazon's data centers."
  default     = ""
}
