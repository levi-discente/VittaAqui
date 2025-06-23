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
	ID       uint   `gorm:"primaryKey" json:"id"`
	Name     string `json:"name"`
	Email    string `gorm:"unique" json:"email"`
	Password string `json:"-"`
	Role     Role   `json:"role"`

	CPF     string `gorm:"unique" json:"cpf"`
	Phone   string `json:"phone"`
	CEP     string `json:"cep"`
	UF      string `json:"uf"`
	City    string `json:"city"`
	Address string `json:"address"`

	CreatedAt           time.Time            `json:"created_at"`
	UpdatedAt           time.Time            `json:"updated_at"`
	DeletedAt           gorm.DeletedAt       `gorm:"index" json:"-"`
	ProfessionalProfile *ProfessionalProfile `gorm:"foreignKey:UserID" json:"professional_profile,omitempty"`
}

type UserRegisterRequest struct {
	Name     string `json:"name" form:"name"`
	Email    string `json:"email" form:"email"`
	Password string `json:"password" form:"password"`
	Role     string `json:"role" form:"role"`

	CPF     string `json:"cpf" form:"cpf"`
	Phone   string `json:"phone" form:"phone"`
	CEP     string `json:"cep" form:"cep"`
	UF      string `json:"uf" form:"uf"`
	City    string `json:"city" form:"city"`
	Address string `json:"address" form:"address"`
}

type UserUpdateRequest struct {
	Name    string `json:"name" form:"name"`
	Email   string `json:"email" form:"email"`
	Role    string `json:"role" form:"role"`
	CPF     string `json:"cpf" form:"cpf"`
	Phone   string `json:"phone" form:"phone"`
	CEP     string `json:"cep" form:"cep"`
	UF      string `json:"uf" form:"uf"`
	City    string `json:"city" form:"city"`
	Address string `json:"address" form:"address"`
}

type UserLoginRequest struct {
	Email    string `json:"email" form:"email"`
	Password string `json:"password" form:"password"`
}

type UserResponse struct {
	ID    uint   `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
	Role  string `json:"role"`

	CPF     string `json:"cpf"`
	Phone   string `json:"phone"`
	CEP     string `json:"cep"`
	UF      string `json:"uf"`
	City    string `json:"city"`
	Address string `json:"address"`
}

type LoginResponse struct {
	Token string       `json:"token"`
	User  UserResponse `json:"user"`
}

func ParseRole(role string) (Role, error) {
	switch Role(role) {
	case RolePatient, RoleProfessional:
		return Role(role), nil
	default:
		return "", errors.New("invalid role")
	}
}

func (u *User) ToUserResponse() *UserResponse {
	if u == nil {
		return nil
	}
	return &UserResponse{
		ID:      u.ID,
		Name:    u.Name,
		Email:   u.Email,
		Role:    string(u.Role),
		CPF:     u.CPF,
		Phone:   u.Phone,
		CEP:     u.CEP,
		UF:      u.UF,
		City:    u.City,
		Address: u.Address,
	}
}
