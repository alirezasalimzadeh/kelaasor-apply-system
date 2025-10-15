from django.core.management.base import BaseCommand, CommandError
from jobs.models import JobPosition, Candidate

class Command(BaseCommand):
    help = "Distribute candidates of job positions into 3 groups (homogeneous by degree/GPA)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--job-id",
            type=int,
            help="Optional JobPosition ID to distribute. If omitted, all jobs are processed.",
        )

    def handle(self, *args, **options):
        job_id = options.get("job_id")
        jobs = JobPosition.objects.all() if not job_id else JobPosition.objects.filter(id=job_id)
        if job_id and not jobs.exists():
            raise CommandError(f"JobPosition with id {job_id} not found.")

        total = 0
        for job in jobs:
            candidates = (
                Candidate.objects.filter(job_position=job)
                .select_related("user__profile")
                .order_by()
            )
            sorted_list = sorted(
                candidates,
                key=lambda c: (str(getattr(c.user.profile, "degree", "") or ""), -(getattr(c.user.profile, "gpa", 0.0)))
            )
            groups = (1, 2, 3)
            for idx, cand in enumerate(sorted_list):
                cand.group = groups[idx % 3]
                cand.save(update_fields=["group"])
            self.stdout.write(self.style.SUCCESS(
                f"Distributed {len(sorted_list)} candidates for job '{job.get_title_display()}'"
            ))
            total += len(sorted_list)

        self.stdout.write(self.style.SUCCESS(f"Done. Total candidates distributed: {total}"))
