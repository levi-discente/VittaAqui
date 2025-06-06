package main

import (
	"log"
	"os"
	"os/exec"
	"os/signal"
	"syscall"
	_ "vittaAqui/docs"
	"vittaAqui/internal/config"
	"vittaAqui/internal/controller"
	"vittaAqui/internal/middlewares"
	"vittaAqui/internal/repositories"
	"vittaAqui/internal/services"
	"vittaAqui/internal/utils"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/joho/godotenv"
	fiberSwagger "github.com/swaggo/fiber-swagger"
)

func main() {

	testCode := exec.Command("go", "test", "./...")
	err := testCode.Run()
	if err != nil {
		log.Fatal(err)
	} else {

	}

	swaggerInit := exec.Command("/home/levirenato/go/bin/swag", "init")

	if err := swaggerInit.Run(); err != nil {
		log.Fatal(err)
	} else {
		log.Println("swagger init success")
	}

	if err := godotenv.Load(); err != nil {
		log.Println("No .env file found, reading environment variables directly.")
	}
	cfg := config.LoadConfig()
	db := utils.ConnectDatabase(cfg)

	professionalRepo := repositories.NewProfessionalProfileRepository(db)
	professionalService := services.NewProfessionalProfileService(professionalRepo)
	professionalHandler := controller.NewProfessionalProfileHandler(professionalService)

	userRepo := repositories.NewUserRepository(db)
	userService := services.NewUserService(userRepo, professionalService)
	userHandler := controller.NewUserHandler(userService, cfg)

	app := fiber.New()

	// 1) Habilita CORS para todas as rotas e todas as origens:
	app.Use(cors.New(cors.Config{
		AllowOrigins: "*", // permite qualquer origem
		AllowMethods: "GET,POST,PUT,DELETE,OPTIONS",
		AllowHeaders: "Origin, Content-Type, Authorization",
	}))

	// 2) (opcional) registra rota de Swagger
	app.Get("/swagger/*", fiberSwagger.WrapHandler)

	// 3) Rotas de autenticação (sem precisar de token)
	auth := app.Group("/auth")
	auth.Post("/register", userHandler.Register)
	auth.Post("/login", userHandler.Login)

	// 4) Rotas de usuário (todas protegidas pelo middleware RequireAuth)
	user := app.Group("/user", middlewares.RequireAuth(cfg.JWTSecret))
	user.Get("/me", userHandler.GetMe)
	user.Put("/me", userHandler.UpdateMe)
	user.Delete("/me", userHandler.DeleteMe)
	user.Get("/:id", userHandler.GetUserByID)
	user.Get("/", userHandler.GetAllUsers)

	// 5) Rotas de perfil profissional
	prof := app.Group("/professional")
	prof.Post("/profile", middlewares.RequireAuth(cfg.JWTSecret), professionalHandler.CreateProfile)
	prof.Get("/profile/user/:user_id", professionalHandler.GetByUserID)
	prof.Get("/profile/:id", professionalHandler.GetByProfessionalID)
	prof.Get("/list", professionalHandler.ListProfessionals)
	prof.Put("/profile/:id", middlewares.RequireAuth(cfg.JWTSecret), professionalHandler.EditProfile)
	prof.Delete("/profile/:id", middlewares.RequireAuth(cfg.JWTSecret), professionalHandler.DeleteProfile)

	srv := app.Listen(":8000")
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	go func() {
		if err := srv; err != nil {
			log.Fatalf("Fiber server error: %v", err)
		}
	}()
	<-c
	log.Println("Gracefully shutting down...")
	if err := app.Shutdown(); err != nil {
		log.Fatalf("Error during shutdown: %v", err)
	}
	log.Println("Server stopped")
}
