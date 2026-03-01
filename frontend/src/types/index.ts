export interface User {
  id: number
  email: string
  created_at: string
}

export interface Photo {
  id: number
  name: string
  filename: string
  upload_date: string
  user_id: number
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
}

export interface LoginResponse {
  access_token: string
  user: User
}

export interface RegisterResponse {
  message: string
  user: User
}

export interface PhotoUploadRequest {
  name: string
  file: File
}

export interface PhotoUploadResponse {
  message: string
  photo: Photo
}

export interface ApiError {
  error: string
}

export type SortOption = 'date_desc' | 'date_asc' | 'name_asc' | 'name_desc'
