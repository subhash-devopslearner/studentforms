from django.db import models
from django.core.exceptions import ValidationError


# ==========================
# Department Model
# ==========================

class Department(models.Model):
    """
    Represents an academic department.
    Examples:
    - Computer Engineering
    - Mechanical Engineering
    - Applied Sciences & Humanities (ASH)
    """

    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=20, unique=True)

    is_academic = models.BooleanField(
        default=True,
        help_text="If False, it is administrative/non-teaching department."
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


# ==========================
# Program Model
# ==========================

class Program(models.Model):
    """
    Examples:
    - BTech (4 years)
    - MBATech (5 years)
    """

    name = models.CharField(max_length=50, unique=True)
    duration_years = models.PositiveSmallIntegerField()

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def total_semesters(self):
        return self.duration_years * 2


# ==========================
# Branch Model
# ==========================

class Branch(models.Model):
    """
    Represents a program-specific academic branch.

    Examples:
    - Computer Engineering (BTech)
    - Computer Engineering (MBATech)
    - IT (BTech)

    In most colleges:
    Department == Branch name
    But department exists independently.
    """

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    program = models.ForeignKey(
        Program,
        on_delete=models.PROTECT,
        related_name="branches"
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="branches"
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['program__name', 'code']
        constraints = [
            models.UniqueConstraint(
                fields=['code', 'program'],
                name='unique_branch_per_program'
            )
        ]

    def __str__(self):
        return f"{self.program} - {self.name}"


# ==========================
# Academic Year Model
# ==========================

class AcademicYear(models.Model):
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()

    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_year']
        constraints = [
            models.UniqueConstraint(
                fields=['start_year', 'end_year'],
                name='unique_academic_year'
            )
        ]

    def clean(self):
        if self.end_year != self.start_year + 1:
            raise ValidationError(
                "End year must be exactly start_year + 1"
            )

    def __str__(self):
        return f"{self.start_year}-{self.end_year}"


# ==========================
# Semester Model
# ==========================

class Semester(models.Model):
    number = models.PositiveSmallIntegerField()

    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name="semesters"
    )

    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="semesters"
    )

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['academic_year__start_year', 'branch__program__name', 'number']
        constraints = [
            models.UniqueConstraint(
                fields=['number', 'branch', 'academic_year'],
                name='unique_semester_per_branch_year'
            )
        ]
        indexes = [
            models.Index(fields=['branch']),
            models.Index(fields=['academic_year']),
        ]

    def clean(self):
        max_semesters = self.branch.program.total_semesters

        if self.number > max_semesters:
            raise ValidationError(
                f"This program allows only {max_semesters} semesters."
            )

        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError(
                    "End date must be after start date."
                )

    def __str__(self):
        return f"{self.branch} - Semester {self.number} ({self.academic_year})"
