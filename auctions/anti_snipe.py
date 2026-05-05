from datetime import timedelta
from django.utils import timezone

SNIPE_WINDOW_SECONDS = 60    # ja solī pēdējās 60 sekundēs
EXTENSION_MINUTES = 3        # pagarina par 3 minūtēm
MAX_EXTENSIONS = 10          # maksimāli 10 pagarinājumi vienai izsolei


def check_and_extend(auction):
    """
    Pārbauda vai solījums notika pēdējās SNIPE_WINDOW_SECONDS sekundēs.
    Ja jā un nav sasniegts MAX_EXTENSIONS — pagarina izsoli.
    Atgriež (pagarināts: bool, jaunais_beigu_laiks: datetime|None).
    """
    if auction.anti_snipe_count >= MAX_EXTENSIONS:
        return False, None

    time_left = auction.ends_at - timezone.now()
    if time_left.total_seconds() <= SNIPE_WINDOW_SECONDS:
        auction.ends_at += timedelta(minutes=EXTENSION_MINUTES)
        auction.anti_snipe_count += 1
        auction.save(update_fields=['ends_at', 'anti_snipe_count'])
        return True, auction.ends_at

    return False, None
