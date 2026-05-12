from django.db import models

# backend models for portfolio app

class Profile(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    subtitle = models.CharField(
        max_length=200,
        help_text="Comma-separated list used by the typed animation",
    )
    hero_text = models.TextField(blank=True)
    about_title = models.CharField(max_length=200, default="About Me")
    about_description = models.TextField(blank=True)

    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    availability = models.CharField(max_length=100, blank=True)

    # stats displayed in profile card
    projects_count = models.PositiveIntegerField(default=0)
    years_experience = models.CharField(max_length=50, blank=True)
    awards_count = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)

    avatar = models.ImageField(upload_to="avatars/", blank=True)
    background = models.ImageField(upload_to="backgrounds/", blank=True)
    cv = models.FileField(upload_to="cv/", blank=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100)
    percent = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.percent}%)"


class DetailItem(models.Model):
    CATEGORY_CHOICES = [
        ("experience", "Experience"),
        ("degree", "Degree"),
        ("location", "Based In"),
        ("email", "Email"),
        ("phone", "Phone"),
        ("availability", "Availability"),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    content = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.get_category_display()}: {self.content}"


class Experience(models.Model):
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200, blank=True)
    duration = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    skills_tags = models.CharField(max_length=300, blank=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} at {self.company_name}"

    @property
    def skills_list(self):
        """Return tags as a list trimmed of whitespace."""
        return [t.strip() for t in self.skills_tags.split(",") if t.strip()]

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} <{self.email}>"

class Education(models.Model):
    year_range = models.CharField(max_length=50)
    degree_level = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    achievement = models.CharField(max_length=200, blank=True)
    achievement_icon = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.title} ({self.year_range})"


class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=100, blank=True)
    featured = models.BooleanField(default=False)
    link = models.URLField(blank=True)
    
    # Pricing and service details for the detail page
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    delivery_time = models.CharField(max_length=100, blank=True, help_text="e.g., '4-6 weeks delivery'")
    revisions = models.CharField(max_length=100, blank=True, help_text="e.g., 'Unlimited revisions'")
    support_duration = models.CharField(max_length=100, blank=True, help_text="e.g., '60 days support'")

    # Optional parent service to allow grouping/hierarchy (e.g. "Music Production" → "Mixing").
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="subservices",
        on_delete=models.CASCADE,
        help_text="Choose a parent service if this is a sub‑service",
    )

    def __str__(self):
        # avoid recursive __str__ calls by using parent's title directly
        if getattr(self, 'parent', None):
            return f"{self.parent.title} → {self.title}"
        return self.title


class Tech_tools(models.Model):
    name = models.CharField(max_length=100)
    tech_tools = models.ForeignKey(
        Service,
        related_name="tech_tools",
        on_delete=models.CASCADE,
        help_text="Select the service this tool is associated with",
    )

    def __str__(self):
        return self.name
    

class customerServices(models.Model):
    icon = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100)
    details = models.TextField(blank=True)
    customer_services = models.ForeignKey(
        Service,    
        related_name="customer_services",
        on_delete=models.CASCADE,
        help_text="Select the service this customer service is associated with",
    )

    def __str__(self):
        return self.name


class PortfolioItem(models.Model):
    CATEGORY_CHOICES = [
        ("solo", "Solo"),
        ("band", "Band"),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to="portfolio/")
    year = models.CharField(max_length=10, blank=True)
    tags = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.title

    @property
    def tags_list(self):
        return [t.strip() for t in self.tags.split(",") if t.strip()]