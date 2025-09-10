# Contributing to Mubaku

We’re excited that you’re interested in contributing to **Mubaku** 🎉  
This document outlines the process for contributing as if this were a fully open-source project.

---

## 📖 Code of Conduct

Be respectful, constructive, and inclusive.  
Everyone is welcome to contribute.

---

## 🛠 How to Contribute

### 1. Fork the Repository

Click the **Fork** button on the top right of the [Mubaku repo](https://github.com/ACHIRIHILARY/mubaku-lifestyle-backend.git).

### 2. Clone Your Fork

```bash
git clone https://github.com/yourusername/mubaku.git
cd mubaku
```

### 3. Set Up Remotes

```bash
git remote add upstream https://github.com/original-owner/mubaku-lifestyle-backend.git
```

Check with:

```bash
git remote -v
```

You should see:

```
origin    https://github.com/yourusername/mubaku.git (fetch)
origin    https://github.com/yourusername/mubaku.git (push)
upstream  https://github.com/ACHIRIHILARY/mubaku-lifestyle-backend.git (fetch)
upstream  https://github.com/ACHIRIHILARY/mubaku-lifestyle-backend.git (push)
```

### 4. Create a Branch

Always work on a feature branch:

```bash
git checkout -b feature/my-new-feature
```

### 5. Make Your Changes

* Write clear, maintainable code
* Follow Django conventions
* Add/update tests if necessary

### 6. Run Tests

```bash
make test
```

Ensure all tests pass before pushing.

### 7. Commit Your Changes

Use descriptive commit messages:

```bash
git add .
git commit -m "Add feature: user booking calendar"
```

### 8. Push to Your Fork

```bash
git push origin feature/my-new-feature
```

### 9. Open a Pull Request

Go to the original repository and click **New Pull Request**.
Choose your branch from your fork and submit it for review.

---

## 🔄 Keeping Your Fork Updated

Before starting new work, always sync with the `upstream` repo:

```bash
git checkout main
git pull upstream main
git push origin main
```

---

## ✅ Guidelines

* Write clear and concise code
* Follow PEP 8 style guidelines
* Include tests for new features
* Keep commits focused and atomic
* Document new functionality in the README if applicable

---

## 💬 Need Help?

Open an [issue](https://github.com/ACHIRIHILARY/mubaku-lifestyle-backend/issues) if you have questions, ideas, or run into problems.


