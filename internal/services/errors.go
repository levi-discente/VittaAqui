package services

import "errors"

var ErrNotProfileOwner = errors.New("unauthorized: not the profile owner")

var ErrEmailAlreadyExists = errors.New("email already registered")

var ErrCPFAlreadyExists = errors.New("cpf already registered")

var ErrInvalidCPF = errors.New("invalid CPF")
