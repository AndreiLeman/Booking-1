from django.core.management.base import BaseCommand, CommandError
from exambookings.models import Booking
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.models import User, Permission
from profiles.models import prettyNameOfUser

import datetime
#import exceptions

# see also https://docs.djangoproject.com/en/dev/howto/custom-management-commands/#howto-custom-management-commands

today = datetime.datetime.today()
cutoffDay = today - datetime.timedelta(days=1)

# appt/test dated older than 2 days are deleted
# appt/test completed are deleted
# anything completed or deleted needs to be in a report emailed to appropriate users daily

perm = Permission.objects.get(codename='exam_center_view')
examCenterStaffEmails = list(set(User.objects.filter(Q(user_permissions=perm) | Q(groups__permissions=perm)).values_list('email', flat=True)))

class ReportEmail():
    fromEmail = 'mrccheng0@example.com'    
    individualReportSubject = "[Exam Center Report]: " + str(today.strftime("%Y %b %d"))
    fullReportSubject = "[Exam Center Full Report]: " + str(today.strftime("%Y %b %d"))
    fullReportRecipientEmails = examCenterStaffEmails

class Command(BaseCommand):
    args = 'none'
    help = 'Clean up exambookings by emailing reports and deleting old appointments'

    def handle(self, *args, **options):
        bookings = Booking.objects.filter(Q(testDate__lt=cutoffDay) | Q(testCompleted=True))
        if bookings.count() == 0:
            return
        
        sortedBookings = bookings.extra(select={'lower_studentFirstName': 'lower(studentFirstName)',
                                                'lower_studentLastName': 'lower(studentLastName)'}).order_by('testDate', 'testPeriod',
                                                                                                             'lower_studentFirstName',
                                                                                                             'lower_studentLastName')

        # full report for exam center
        fullReport = ""
        for booking in sortedBookings:
            fullReport += "- "
            fullReport += str(booking)
            fullReport += " (" + str(prettyNameOfUser(booking.courseTeacher)) + ")"
            fullReport += "\n"
        send_mail(ReportEmail.fullReportSubject, fullReport, ReportEmail.fromEmail,
                  ReportEmail.fullReportRecipientEmails, fail_silently=True)

        # individual reports to teachers
        courseTeachersPks = set(bookings.values_list('courseTeacher', flat=True))
        bookingsReported = []
        for pk in courseTeachersPks:
            try:
                courseTeacherEmail = User.objects.get(id__iexact=pk).email
                report = ""
                bookingsReportedToTeacher = [] # temp var to ensure email is sent out before deleting these bookings
                for booking in sortedBookings.filter(courseTeacher = pk):
                    report += "- "
                    report += str(booking)
                    report += "\n"
                    bookingsReportedToTeacher.append(booking)
                send_mail(ReportEmail.individualReportSubject, report, ReportEmail.fromEmail,
                          [courseTeacherEmail], fail_silently=False)
                bookingsReported += bookingsReportedToTeacher
            except:
                pass

        # when all done reporting, DELETE
        for booking in bookingsReported:
            try:
                booking.delete()
            except:
                pass

#        self.stdout.write("hi")
