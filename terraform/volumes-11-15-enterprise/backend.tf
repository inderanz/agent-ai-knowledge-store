terraform {
  # Supply bucket/prefix at init time; never hard-code a customer state location.
  backend "gcs" {}
}
