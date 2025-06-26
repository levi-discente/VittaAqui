package services

import (
	"errors"

	"github.com/levirenato/VittaAqui/internal/models"
	"github.com/levirenato/VittaAqui/internal/repositories"
)

type ProfessionalProfileService struct {
	repo *repositories.ProfessionalProfileRepository
}

type ProfessionalProfileServiceInterface interface {
	CreateProfile(userID uint, data *models.ProfessionalProfile) error
	GetByUserID(userID uint) (*models.ProfessionalProfile, error)
	GetByProfessionalID(profileID uint) (*models.ProfessionalProfile, error)
	ListProfessionals(category, name string, tags []string, onlyOnline, onlyPresential *bool) ([]models.ProfessionalProfile, error)
	EditProfile(userID, profileID uint, data *models.ProfessionalProfile) error
	DeleteProfile(userID, profileID uint) error
}

func NewProfessionalProfileService(repo *repositories.ProfessionalProfileRepository) *ProfessionalProfileService {
	return &ProfessionalProfileService{repo}
}

func (s *ProfessionalProfileService) CreateProfile(userID uint, data *models.ProfessionalProfile) error {
	existing, _ := s.repo.GetByUserID(userID)
	if existing != nil && existing.ID != 0 {
		return errors.New("profile already exists")
	}
	data.UserID = userID
	return s.repo.Create(data)
}

func (s *ProfessionalProfileService) GetByUserID(userID uint) (*models.ProfessionalProfile, error) {
	return s.repo.GetByUserID(userID)
}

func (s *ProfessionalProfileService) GetByProfessionalID(profileID uint) (*models.ProfessionalProfile, error) {
	return s.repo.GetByProfessionalID(profileID)
}

func (s *ProfessionalProfileService) ListProfessionals(category, name string, tags []string, onlyOnline, onlyPresential *bool) ([]models.ProfessionalProfile, error) {
	return s.repo.ListProfessionals(category, name, tags, onlyOnline, onlyPresential)
}

func (s *ProfessionalProfileService) EditProfile(userID, profileID uint, data *models.ProfessionalProfile) error {
	profile, err := s.repo.GetByProfessionalID(profileID)
	if err != nil {
		return errors.New("profile not found")
	}
	if profile.UserID != userID {
		return errors.New("unauthorized: not the profile owner")
	}
	// Atualiza os campos permitidos
	profile.Bio = data.Bio
	profile.Category = data.Category
	profile.Services = data.Services
	profile.Price = data.Price
	profile.OnlyOnline = data.OnlyOnline
	profile.OnlyPresential = data.OnlyPresential
	profile.Tags = data.Tags

	return s.repo.Edit(profile)
}

// Deleta perfil profissional (apenas o owner pode deletar)
func (s *ProfessionalProfileService) DeleteProfile(userID, profileID uint) error {
	profile, err := s.repo.GetByProfessionalID(profileID)
	if err != nil {
		return errors.New("profile not found")
	}
	if profile.UserID != userID {
		return errors.New("unauthorized: not the profile owner")
	}
	return s.repo.Delete(profileID)
}
