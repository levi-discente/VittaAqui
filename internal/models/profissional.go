package models

import (
	"time"

	"gorm.io/gorm"
)

type ProfessionalCategory string

const (
	CategoryNutritionist        ProfessionalCategory = "nutritionist"
	CategoryPersonalTrainer     ProfessionalCategory = "personal_trainer"
	CategoryPhysician           ProfessionalCategory = "physician"
	CategoryPsychologist        ProfessionalCategory = "psychologist"
	CategoryPhysiotherapist     ProfessionalCategory = "physiotherapist"
	CategoryOccupationalTherapy ProfessionalCategory = "occupational_therapy"
	CategoryElderlyCare         ProfessionalCategory = "elderly_care"
	CategoryDoctor              ProfessionalCategory = "doctor"
)

type ProfileTag struct {
	ID        uint `gorm:"primaryKey"`
	Name      string
	ProfileID uint
}

type ProfessionalRating struct {
	ID        uint `gorm:"primaryKey"`
	ProfileID uint
	UserID    uint
	Note      float64
	Comment   string
	createdAt time.Time
	updatedAt time.Time
}

type ProfessionalProfile struct {
	gorm.Model
	UserID                     uint `gorm:"uniqueIndex"`
	User                       User `gorm:"foreignKey:UserID"`
	Bio                        string
	Category                   ProfessionalCategory
	ProfissionalIdentification string `gorm:"uniqueIndex"`
	Services                   string
	Price                      float64
	Tags                       []ProfileTag `gorm:"foreignKey:ProfileID"`
	OnlyOnline                 bool
	OnlyPresential             bool
	Rating                     float64
	NumReviews                 uint
}

type ProfessionalProfileResponse struct {
	ID                         uint     `json:"id"`
	UserID                     uint     `json:"user_id"`
	UserName                   string   `json:"user_name"`
	Email                      string   `json:"email"`
	Phone                      string   `json:"phone"`
	Cep                        string   `json:"cep"`
	UF                         string   `json:"uf"`
	City                       string   `json:"city"`
	Address                    string   `json:"address"`
	Bio                        string   `json:"bio"`
	Category                   string   `json:"category"`
	ProfissionalIdentification string   `json:"profissional_identification"`
	Services                   string   `json:"services"`
	Price                      float64  `json:"price"`
	Tags                       []string `json:"tags"`
	OnlyOnline                 bool     `json:"only_online"`
	OnlyPresential             bool     `json:"only_presential"`
	Rating                     float64  `json:"rating"`
	NumReviews                 uint     `json:"num_reviews"`
}

func ToProfessionalProfileResponse(profile *ProfessionalProfile) ProfessionalProfileResponse {
	tags := make([]string, len(profile.Tags))
	for i, tag := range profile.Tags {
		tags[i] = tag.Name
	}
	return ProfessionalProfileResponse{
		ID:                         profile.ID,
		UserID:                     profile.UserID,
		UserName:                   profile.User.Name,
		Email:                      profile.User.Email,
		Phone:                      profile.User.Phone,
		Cep:                        profile.User.CEP,
		UF:                         profile.User.UF,
		City:                       profile.User.City,
		Address:                    profile.User.Address,
		Bio:                        profile.Bio,
		Category:                   string(profile.Category),
		ProfissionalIdentification: profile.ProfissionalIdentification,
		Services:                   profile.Services,
		Price:                      profile.Price,
		Tags:                       tags,
		OnlyOnline:                 profile.OnlyOnline,
		OnlyPresential:             profile.OnlyPresential,
		Rating:                     profile.Rating,
		NumReviews:                 profile.NumReviews,
	}
}
