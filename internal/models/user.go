package models

import (
	"errors"
	"time"

	"gorm.io/gorm"
)

type Role string

const (
	RolePatient      Role = "patient"
	RoleProfessional Role = "professional"
)

type User struct {
	ID                  uint   `gorm:"primaryKey" json:"id"`
	Name                string `json:"name"`
	Email               string `gorm:"unique" json:"email"`
	Password            string `json:"-"`
	Role                Role
	CreatedAt           time.Time
	UpdatedAt           time.Time
	DeletedAt           gorm.DeletedAt       `gorm:"index" json:"-"`
	ProfessionalProfile *ProfessionalProfile `gorm:"foreignKey:UserID"`
}

type UserRegisterRequest struct {
	Name     string `json:"name"`
	Email    string `json:"email"`
	Password string `json:"password"`
	Role     string `json:"role"`
}
type UserLoginRequest struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}
type LoginResponse struct {
	Token string `json:"token"`
}
type UserResponse struct {
	ID    uint   `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
	Role  string `json:"role"`
}
type UserUpdateRequest struct {
	Name  string `json:"name"`
	Email string `json:"email"`
	Role  string `json:"role"`
}

func ParseRole(role string) (Role, error) {
	switch Role(role) {
	case RolePatient, RoleProfessional:
		return Role(role), nil
	default:
		return "", errors.New("invalid role")
	}
}
