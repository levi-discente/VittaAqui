package services

import (
	"errors"

	"github.com/levirenato/VittaAqui/internal/models"
	"github.com/levirenato/VittaAqui/internal/repositories"
	"github.com/levirenato/VittaAqui/internal/utils"

	"golang.org/x/crypto/bcrypt"
)

type UserService struct {
	repo               *repositories.UserRepository
	profProfileService *ProfessionalProfileService
}

type UserServiceInterface interface {
	Register(req *models.UserRegisterRequest, bio, category string) error
	Login(email, password string) (*models.User, error)
	GetByID(id uint) (*models.User, error)
	UpdateProfile(id uint, req *models.UserUpdateRequest) (*models.User, error)
	DeleteUser(id uint) error
	GetAll() ([]models.User, error)
}

func NewUserService(repo *repositories.UserRepository, profProfileService *ProfessionalProfileService) *UserService {
	return &UserService{repo, profProfileService}
}

func (s *UserService) Register(req *models.UserRegisterRequest, bio, category string) error {
	if !utils.IsValidCPF(req.CPF) {
		return ErrInvalidCPF
	}

	existingByCPF, _ := s.repo.FindByCPF(req.CPF)
	if existingByCPF != nil {
		return ErrCPFAlreadyExists
	}

	existingByEmail, _ := s.repo.FindByEmail(req.Email)
	if existingByEmail != nil {
		return ErrEmailAlreadyExists
	}

	hashed, err := bcrypt.GenerateFromPassword([]byte(req.Password), bcrypt.DefaultCost)
	if err != nil {
		return err
	}

	role, err := models.ParseRole(req.Role)
	if err != nil {
		return err
	}

	user := &models.User{
		Name:     req.Name,
		Email:    req.Email,
		Password: string(hashed),
		Role:     role,
		CPF:      req.CPF,
		Phone:    req.Phone,
		CEP:      req.CEP,
		UF:       req.UF,
		City:     req.City,
		Address:  req.Address,
	}

	if err := s.repo.Create(user); err != nil {
		return err
	}

	if role == models.RoleProfessional {
		profile := &models.ProfessionalProfile{
			UserID:   user.ID,
			Bio:      bio,
			Category: models.ProfessionalCategory(category),
		}
		_ = s.profProfileService.CreateProfile(user.ID, profile)
	}

	return nil
}

func (s *UserService) Login(email, password string) (*models.User, error) {
	user, err := s.repo.FindByEmail(email)
	if err != nil {
		return nil, errors.New("user not found")
	}
	if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(password)); err != nil {
		return nil, errors.New("invalid password")
	}
	return user, nil
}

func (s *UserService) GetByID(id uint) (*models.User, error) {
	return s.repo.FindByID(id)
}

func (s *UserService) UpdateProfile(id uint, req *models.UserUpdateRequest) (*models.User, error) {
	user, err := s.repo.FindByID(id)
	if err != nil {
		return nil, err
	}

	user.Name = req.Name
	user.Email = req.Email
	user.Role = models.Role(req.Role)

	user.CPF = req.CPF
	user.Phone = req.Phone
	user.CEP = req.CEP
	user.UF = req.UF
	user.City = req.City
	user.Address = req.Address

	err = s.repo.Update(user)
	return user, err
}

func (s *UserService) DeleteUser(id uint) error {
	return s.repo.Delete(id)
}

func (s *UserService) GetAll() ([]models.User, error) {
	return s.repo.FindAll()
}
