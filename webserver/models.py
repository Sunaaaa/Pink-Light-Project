from django.db import models

# Create your models here.
class Train(models.Model):
    train_no = models.CharField(max_length=10)
    slot_no = models.CharField(max_length=10)
    seat_no = models.CharField(max_length=10)
    empty = models.BooleanField()

    def __str__(self):
        return f'[{self.train_no}] {self.slot_no} 번칸 {self.seat_no} : 사용여부: {self.empty}'


class Notification(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # train = models.ForeignKey(Train, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.pk}알림] {self.content} : {self.created_at}에 생성'
