package queue

import (
	"encoding/json"
)

type Job struct {
	ID              string
	Method          string
	Params          json.RawMessage
	InjectedContext string
}
