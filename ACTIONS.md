## 🚀 Workflows Overview

### 1. **CI/CD Pipeline** (`.github/workflows/ci-cd.yml`)
**Triggers:** Push to `main`/`develop`, Pull Requests
**Features:**
- ✅ Code quality checks (Black, isort, flake8, mypy)
- 🔒 Security audits (Bandit, Safety)
- 🧪 Unit & integration tests with coverage
- 🐳 Docker build & security scan
- ⚡ Performance testing with Locust
- 🚀 Automated deployment to staging/production

### 2. **Security Scan** (`.github/workflows/security-scan.yml`)
**Triggers:** Daily schedule, Push to `main`, Pull Requests
**Features:**
- 🔍 Dependency vulnerability scanning
- 🔎 CodeQL security analysis
- 🐳 Docker image security scan with Trivy
- 🔐 Secret scanning with TruffleHog
- ⚖️ License compliance checking
- 🛡️ API security testing with OWASP ZAP

### 3. **Release Management** (`.github/workflows/release.yml`)
**Triggers:** Git tags (`v*.*.*`), Manual workflow dispatch
**Features:**
- 🎯 Automated release preparation
- 🏗️ Multi-architecture Docker builds
- 🔒 Container image signing with Cosign
- 📝 Automated release notes generation
- 📦 GitHub release creation
- 🚀 Production deployment

### 4. **Deployment** (`.github/workflows/deploy.yml`)
**Triggers:** Release published, Manual workflow dispatch
**Features:**
- 🔍 Pre-deployment security checks
- 🧪 Blue-green deployment to staging
- 🚀 Production deployment with rollback
- 🔄 Automated rollback on failure
- 📢 Deployment notifications

## 🔧 Setup Requirements

### Repository Secrets
Add these secrets to your GitHub repository (`Settings > Secrets and variables > Actions`):

```bash
# External API Keys (for testing)
GEMINI_API_KEY_TEST=your_test_gemini_api_key
BRAVE_SEARCH_API_KEY_TEST=your_test_brave_search_api_key

# Production API Keys
GEMINI_API_KEY=your_production_gemini_api_key
BRAVE_SEARCH_API_KEY=your_production_brave_search_api_key

# Kubernetes Configuration (base64 encoded)
KUBECONFIG_STAGING=base64_encoded_staging_kubeconfig
KUBECONFIG_PRODUCTION=base64_encoded_production_kubeconfig

# Container Registry
GITHUB_TOKEN=automatically_provided_by_github

# Monitoring & Notifications
SLACK_WEBHOOK_URL=your_slack_webhook_url
DISCORD_WEBHOOK_URL=your_discord_webhook_url
```

### Environment Variables
Configure these in your deployment environments:

```bash
# Application
SECRET_KEY=your_super_secure_secret_key
ENVIRONMENT=production
DEBUG=false

# Database
DATABASE_URL=postgresql://user:password@host:port/database
MONGODB_URL=mongodb://user:password@host:port/database

# External APIs
GEMINI_API_KEY=your_gemini_api_key
BRAVE_SEARCH_API_KEY=your_brave_search_api_key
```

## 📊 Pipeline Stages

### Code Quality Stage
1. **Black** - Code formatting
2. **isort** - Import sorting
3. **flake8** - Linting
4. **mypy** - Type checking
5. **Bandit** - Security analysis
6. **Safety** - Dependency vulnerability check

### Testing Stage
1. **Unit Tests** - pytest with coverage
2. **Integration Tests** - API endpoint testing
3. **Performance Tests** - Load testing with Locust
4. **Security Tests** - OWASP ZAP scanning

### Build Stage
1. **Docker Build** - Multi-stage build
2. **Security Scan** - Trivy vulnerability scan
3. **Image Push** - GitHub Container Registry
4. **Image Signing** - Cosign signature

### Deployment Stage
1. **Pre-deployment Checks** - Health and security validation
2. **Blue-Green Deployment** - Zero-downtime deployment
3. **Health Verification** - Post-deployment testing
4. **Rollback** - Automatic rollback on failure

## 🏃‍♂️ Running Workflows

### Manual Triggers
Some workflows can be triggered manually:

```bash
# Trigger deployment
gh workflow run deploy.yml -f environment=staging -f tag=v1.0.0

# Trigger release
gh workflow run release.yml -f version=v1.0.0 -f prerelease=false

# Trigger security scan
gh workflow run security-scan.yml
```

### Automatic Triggers
Workflows trigger automatically on:
- **Push to main/develop** → CI/CD pipeline
- **Pull Request** → CI/CD pipeline + security scan
- **Git tag (v*.*.*)** → Release workflow
- **Release published** → Deployment workflow
- **Daily at 2 AM UTC** → Security scan

## 📈 Monitoring & Notifications

### Artifacts & Reports
Each workflow generates artifacts:
- 📊 Test coverage reports
- 🔒 Security scan results
- 📋 License compliance reports
- ⚡ Performance test results
- 📝 Release notes

### Status Badges
Add these badges to your README:

```markdown
![CI/CD](https://github.com/your-org/vulntrack-backend/workflows/CI%2FCD%20Pipeline/badge.svg)
![Security](https://github.com/your-org/vulntrack-backend/workflows/Security%20Scan/badge.svg)
![Release](https://github.com/your-org/vulntrack-backend/workflows/Release/badge.svg)
```

## 🛠️ Customization

### Adding New Checks
To add new quality checks, modify `.github/workflows/ci-cd.yml`:

```yaml
- name: 🔍 Your Custom Check
  run: |
    poetry run your-custom-tool app/
```

### Environment-Specific Deployments
To add new environments, create new workflow files:
- `.github/workflows/deploy-staging.yml`
- `.github/workflows/deploy-production.yml`

### Custom Notifications
Add notification steps to workflows:

```yaml
- name: 📢 Slack Notification
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

## 🚨 Troubleshooting

### Common Issues

1. **Test Failures**
   - Check test logs in workflow artifacts
   - Verify environment variables are set
   - Ensure external API keys are valid

2. **Security Scan Failures**
   - Review Trivy and Bandit reports
   - Update vulnerable dependencies
   - Add security exceptions if needed

3. **Deployment Failures**
   - Verify Kubernetes configuration
   - Check container registry access
   - Validate environment secrets

4. **Performance Issues**
   - Review Locust performance reports
   - Optimize database queries
   - Scale application resources

### Debug Mode
Enable debug mode by adding to workflow:

```yaml
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

## 📚 Best Practices

1. **Security First**
   - Never commit secrets to repository
   - Use encrypted secrets for sensitive data
   - Regular security scans and updates

2. **Test Everything**
   - Comprehensive test coverage (>90%)
   - Integration tests for all endpoints
   - Performance tests for critical paths

3. **Automated Quality**
   - Code formatting and linting
   - Type checking and security analysis
   - Dependency vulnerability scanning

4. **Zero-Downtime Deployments**
   - Blue-green deployment strategy
   - Health checks and rollback mechanisms
   - Database migration strategies

5. **Monitoring & Observability**
   - Comprehensive logging
   - Performance monitoring
   - Error tracking and alerting
