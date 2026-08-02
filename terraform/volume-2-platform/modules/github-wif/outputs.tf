output "provider" {
  value = {
    for mode, provider in google_iam_workload_identity_pool_provider.github :
    mode => {
      name                 = provider.name
      repository_principal = local.repository_principals[mode]
    }
  }
}
