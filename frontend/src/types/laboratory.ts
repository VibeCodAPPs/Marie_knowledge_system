export interface Laboratory {
  id: number;
  name: string;
  description?: string;
  color: string;
  icon: string;
  is_active: boolean;
  is_archived: boolean;
  settings: Record<string, any>;
  lightweight_model?: string;
  deep_model?: string;
  concept_count: number;
  source_count: number;
  study_hours: number;
  created_at: string;
  updated_at: string;
  display_name: string;
}

export interface CreateLaboratoryRequest {
  name: string;
  description?: string;
  color?: string;
  icon?: string;
  lightweight_model?: string;
  deep_model?: string;
}

export interface UpdateLaboratoryRequest extends Partial<CreateLaboratoryRequest> {
  is_active?: boolean;
  is_archived?: boolean;
  settings?: Record<string, any>;
}
