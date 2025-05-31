package services

import "errors"

var ErrNotProfileOwner = errors.New("unauthorized: not the profile owner")
