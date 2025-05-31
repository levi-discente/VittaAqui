package main

import (
	"log"
	_ "vittaAqui/docs"
	"vittaAqui/internal/config"
	"vittaAqui/internal/handlers"
	"vittaAqui/internal/middlewares"
	"vittaAqui/internal/repositories"
	"vittaAqui/internal/services"
	"vittaAqui/internal/utils"

	"github.com/gofiber/fiber/v2"
	"github.com/joho/godotenv"
	fiberSwagger "github.com/swaggo/fiber-swagger"
)

// @title vittaAqui API
// @version 1.0
// @description Documentação da API vittaAqui
// @securityDefinitions.apikey BearerAuth
// @in header
// @name Authorization

func main() {
	if err := godotenv.Load(); err != nil {
		log.Println("No .env file found, reading environment variables directly.")
	}
	cfg := config.LoadConfig()
	db := utils.ConnectDatabase(cfg)

	professionalRepo := repositories.NewProfessionalProfileRepository(db)
	professionalService := services.NewProfessionalProfileService(professionalRepo)
	professionalHandler := handlers.NewProfessionalProfileHandler(professionalService)

	userRepo := repositories.NewUserRepository(db)
	userService := services.NewUserService(userRepo, professionalService)
	userHandler := handlers.NewUserHandler(userService, cfg)

	app := fiber.New()

	// Swagger
	app.Get("/swagger/*", fiberSwagger.WrapHandler)

	// Rotas de autenticação
	auth := app.Group("/auth")
	auth.Post("/register", userHandler.Register)
	auth.Post("/login", userHandler.Login)

	// Rotas de usuário (todas protegidas pelo middleware de autenticação)
	user := app.Group("/user", middlewares.RequireAuth(cfg.JWTSecret))

	user.Get("/me", userHandler.GetMe)
	user.Put("/me", userHandler.UpdateMe)
	user.Delete("/me", userHandler.DeleteMe)

	// Só admin ou o próprio usuário deve acessar as rotas abaixo (faça a checagem nos handlers!)
	user.Get("/:id", userHandler.GetUserByID)
	user.Get("/", userHandler.GetAllUsers)

	prof := app.Group("/professional")

	prof.Post("/profile", middlewares.RequireAuth(cfg.JWTSecret), professionalHandler.CreateProfile)
	prof.Get("/profile/user/:user_id", professionalHandler.GetByUserID)
	prof.Get("/profile/:id", professionalHandler.GetByProfessionalID)
	prof.Get("/list", professionalHandler.ListProfessionals)
	prof.Put("/profile/:id", middlewares.RequireAuth(cfg.JWTSecret), professionalHandler.EditProfile)
	prof.Delete("/profile/:id", middlewares.RequireAuth(cfg.JWTSecret), professionalHandler.DeleteProfile)

	log.Fatal(app.Listen(":8000"))
}
