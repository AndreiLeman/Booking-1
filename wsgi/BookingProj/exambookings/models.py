from django.db import models
from django.core.urlresolvers import reverse
#import datetime

#from profiles.models import BaseProfile
from django.contrib.auth.models import User

# Create your models here.
# class StudentProfile(models.Model):
#     baseProfile = models.OneToOneField(BaseProfile,
#                                 unique=True,
#                                 verbose_name= ('base_profile'),
#                                 related_name='studentProfile')
#     grade = models.IntegerField(max_length=2)
#     accomodations = models.TextField(max_length=400)

#     def __unicode__(self):
#         return (self.baseProfile.user.first_name + " " + self.baseProfile.user.last_name + " profile")
    
# class Test(models.Model):
#     name = models.CharField(max_length=40)
#     duration = models.IntegerField(max_length=4)
#     materialRequired = models.TextField(max_length=400)
    
#     def __unicode__(self):
#         return (self.name + " and " + str(self.duration))

# class Course(models.Model):
#     subject = models.CharField(max_length=40)
#     level = models.CharField(max_length=6)
#     students = models.ManyToManyField(StudentProfile, through='StudentBelongsToCourse')
#     tests = models.ManyToManyField(Test, through='CourseAssessedByTest')
#     def __unicode__(self):
#         return (self.subject + " @ " + self.level)

# class WorkPeriod(models.Model):
#     start = models.DateTimeField()
#     end = models.DateTimeField()
    
#     def __unicode__(self):
#         return (str(self.start) + " to " + str(self.end))

# class ExamCenter(models.Model):
#     roomNumber = models.CharField(max_length=15)
#     deskSeats = models.IntegerField(max_length=4)
#     computerSeats = models.IntegerField(max_length=4)
#     materialAvailable = models.TextField(max_length=400)
#     students = models.ManyToManyField(StudentProfile, through='StudentAssignedToExamCenter')
#     workPeriods = models.ManyToManyField(WorkPeriod, through='WorkPeriodAssignedToExamCenter')
    
#     def __unicode__(self):
#         return (self.roomNumber + " with " + str(self.deskSeats) + " and  " + str(self.computerSeats) + " seats")
        
# class StaffProfile(models.Model):
#     baseProfile = models.OneToOneField(BaseProfile,
#                                 unique=True,
#                                 verbose_name= ('base_profile'),
#                                 related_name='staffProfile')
#     courses = models.ManyToManyField(Course, through='StaffTeachingCourse')
#     workPeriods = models.ManyToManyField(WorkPeriod, through='StaffHasAWorkPeriod')
#     speciality = models.TextField(max_length=400)

#     def __unicode__(self):
#         return (self.baseProfile.user.first_name + " " + self.baseProfile.user.last_name + " profile")    


# class Booking(models.Model):
#     studentProfile = models.ForeignKey(StudentProfile)
#     course = models.ForeignKey(Course)
#     test = models.ForeignKey(Test)
#     examCenter = models.ForeignKey(ExamCenter)
#     courseTeacherProfile = models.ForeignKey(StaffProfile)
#     workPeriod = models.ForeignKey(WorkPeriod)

#     class Meta:
#         permissions = (
#             ("teacher_view", "Can view teacher's own bookings"),
#             ("exam_center_view", "Can view all bookings"),
#             )

_PERIOD_TUTORIAL = 830
_PERIOD_ONE = 900
_PERIOD_TWO = 1030
_PERIOD_LUNCH = 1200
_PERIOD_THREE = 1230
_PERIOD_FOUR = 1400
_PERIOD_AFTERSCHOOL = 1530
_TEST_PERIOD_CHOICES = (
    (_PERIOD_TUTORIAL, 'Tutorial Time'),
    (_PERIOD_ONE, 'Period 1'),
    (_PERIOD_TWO, 'Period 2'),
    (_PERIOD_LUNCH, 'Lunch Time'),
    (_PERIOD_THREE, 'Period 3'),
    (_PERIOD_FOUR, 'Period 4'),
    (_PERIOD_AFTERSCHOOL, 'After School'),
    )
PERIOD_TIME_NAME_MAP = dict(_TEST_PERIOD_CHOICES)

class Booking(models.Model):
    GRADE_TEN = 10
    GRADE_ELEVEN = 11
    GRADE_TWELVE = 12
    STUDENT_GRADE_CHOICES = (
        (GRADE_TEN, '10'),
        (GRADE_ELEVEN, '11'),
        (GRADE_TWELVE, '12'),
        )
    
    EXAM_CENTER_RM_100 = '100A'
    EXAM_CENTER_CHOICES = (
        (EXAM_CENTER_RM_100, "Main Exam Center - Rm 100"),
        )
    
    PERIOD_TUTORIAL = _PERIOD_TUTORIAL
    PERIOD_ONE = _PERIOD_ONE
    PERIOD_TWO = _PERIOD_TWO
    PERIOD_LUNCH = _PERIOD_LUNCH
    PERIOD_THREE = _PERIOD_THREE
    PERIOD_FOUR = _PERIOD_FOUR
    PERIOD_AFTERSCHOOL = _PERIOD_AFTERSCHOOL
    TEST_PERIOD_CHOICES = _TEST_PERIOD_CHOICES

    # studentProfile = models.ForeignKey(StudentProfile)
    studentFirstName = models.CharField(max_length=30,
                                        verbose_name="Student's First Name")
    studentLastName = models.CharField(max_length=30,
                                       verbose_name="Student's Last Name (Initial)")
    studentGrade = models.IntegerField(choices=STUDENT_GRADE_CHOICES,
                                       default=GRADE_TEN,
                                       verbose_name="Student's Grade")
    
    # course = models.ForeignKey(Course)
    testCourseName = models.CharField(max_length=40,
                                      verbose_name="Course Name")

    # courseTeacherProfile = models.ForeignKey(StaffProfile)
    courseTeacher = models.ForeignKey(User,
                                      verbose_name="Course Teacher")
    
    # test = models.ForeignKey(Test)
    testName = models.CharField(max_length=40,
                                verbose_name="Test Name")
    testDuration = models.CharField(max_length=40,
                                    verbose_name="Test Duration")
    testDate = models.DateField(verbose_name="Test on Date")    

    # workPeriod = models.ForeignKey(WorkPeriod)
    testPeriod = models.IntegerField(choices=TEST_PERIOD_CHOICES,
                                     default=PERIOD_AFTERSCHOOL,
                                     verbose_name="Test in Period")
    
    # examCenter = models.ForeignKey(ExamCenter)
    examCenter = models.CharField(max_length=5,
                                  choices=EXAM_CENTER_CHOICES,
                                  default=EXAM_CENTER_RM_100,
                                  verbose_name="Exam Room")


    # accomodations
    extendedTimeAccomodation = models.BooleanField(verbose_name="Extended Time")
    computerAccomodation = models.BooleanField(verbose_name="Computer")
    scribeAccomodation = models.BooleanField(verbose_name="Scribe")
    enlargementsAccomodation = models.BooleanField(verbose_name="Enlargements")
    readerAccomodation = models.BooleanField(verbose_name="Reader")
    isolationQuietAccomodation = models.BooleanField(verbose_name="Isolation/Quiet")

    # allowances
    ellDictionaryAllowance = models.BooleanField(verbose_name="ELL Dictionary")
    calculatorManipulativesAllowance = models.BooleanField(verbose_name="Calculator/Manipulatives")
    openBookNotesAllowance = models.BooleanField(verbose_name="Open book/Notes")
    computerInternetAllowance = models.BooleanField(verbose_name="Computer/Internet")
    englishDictionaryThesaurusAllowance = models.BooleanField(verbose_name="ELL Dictionary/Thesaurus")
    otherAllowances = models.CharField(max_length=200, blank=True, verbose_name="Other Allowances")

    testCompleted = models.BooleanField(verbose_name="Test Taken")

    class Meta:
        permissions = (
            ("teacher_view", "Can view teacher's own bookings"),
            ("exam_center_view", "Can view all bookings"),
            )
        verbose_name = "Exam Appointment"
        unique_together = (('studentFirstName',
                            'studentLastName',
                            'studentGrade',
                            'testCourseName',
                            'courseTeacher',
                            'testName',
                            'testDate',
                            'testPeriod',),)

    @classmethod
    def getFieldnamesStdOrder(cls):
        return ["studentFirstName",
                "studentLastName",
                'studentGrade',
                "testCourseName",
                "courseTeacher",
                'testName',
                'testDuration',
                'testDate',
                "testPeriod",
                "examCenter",
                'extendedTimeAccomodation',
                'computerAccomodation',
                'scribeAccomodation',
                'enlargementsAccomodation',
                'readerAccomodation',
                'isolationQuietAccomodation',
                'ellDictionaryAllowance',
                'calculatorManipulativesAllowance',
                'openBookNotesAllowance',
                'computerInternetAllowance',
                'englishDictionaryThesaurusAllowance',
                'otherAllowances',
                'testCompleted']

    def fieldDataOf(self, fieldNameStr):
        f = self._meta.get_field(fieldNameStr)
        attname = f.get_attname()
        data= {'name': fieldNameStr,
               'attname': attname, # could be different from fieldNameStr, e.g. courseTeacher_id
               'verbose_name': f.verbose_name,
               'help_text': f.help_text,
               'value': eval("self."+attname)}
        if fieldNameStr  == 'courseTeacher':
            data['value'] = self.courseTeacher # avoids showing foreign key id
        elif fieldNameStr == 'testPeriod':
            data['value'] = PERIOD_TIME_NAME_MAP[data['value']]
        return data

    def getNormalizedDataOfFields(self, fieldNamesList=None, orderedFields=False, incl_false_bool_fields=False):
        """ returns fields indicated in fieldNamesList using fieldDataOf()
        in either an ordered list or dict depending on orderedFields
        """
        if fieldNamesList == None:
            fieldNamesList = Booking.getFieldnamesStdOrder()
            
        if orderedFields:
            data = []
        else:
            data = {}
            
        for fieldname in fieldNamesList:
            fieldData = self.fieldDataOf(fieldname)
            if incl_false_bool_fields or fieldData['value'] != False:
                if orderedFields:
                    data.append(fieldData)
                else:
                    data.update({fieldname: fieldData})
        return data

    @classmethod
    def getAllObjectsDataNormalizedForUser(cls, user, incl_false_bool_fields = False, orderedFields = True, sortAppts = True):
        """ returns list of dictionaries representing a booking
        appointment the user can view.
        each booking is either a list if orderedFields == True,
        else is a dict
        """
        if (user.has_perm('exambookings.exam_center_view')):
            bookings = cls.objects.all()
        elif (user.has_perm('exambookings.teacher_view')):
            bookings = cls.objects.filter(courseTeacher=user)
        else:
            bookings = []

            if sortAppts and bookings != []:
                bookings = bookings.extra(select={'lower_studentFirstName': 'lower(studentFirstName)',
                                                  'lower_studentLastName': 'lower(studentLastName)'}).order_by('testDate', 'testPeriod',
                                                                                                               'lower_studentFirstName',
                                                                                                               'lower_studentLastName')
        bookings_list = []
        for booking in bookings:
            bookingObj = {'meta':'', 'data':''}
            bookingObj['meta'] = {'editUrl':{'value':reverse('update_booking',
                                                             kwargs={'pk':booking.pk}),
                                             'verbose_name': "Edit Booking",
                                             'help_text': '',
                                             'name': 'editUrl'},
                                  'setCompletedUrl': {'value':reverse('set_booking_completed',
                                                                      kwargs={'pk':booking.pk}),
                                                      'verbose_name': "Test Taken",
                                                      'help_text': '',
                                                      'name': 'setCompletedUrl'},
                                  'deleteUrl': {'value':reverse('delete_booking',
                                                                kwargs={'pk':booking.pk}),
                                                'verbose_name': "Delete Booking",
                                                'help_text': '',
                                                'name': 'deleteUrl'}
                                  }
            bookingObj['data'] = booking.getNormalizedDataOfFields(orderedFields=orderedFields, incl_false_bool_fields=incl_false_bool_fields)
            bookings_list.append(bookingObj)
        return bookings_list


    


#Relations
# class StudentBelongsToCourse(models.Model):
#     student = models.ForeignKey(StudentProfile)
#     course = models.ForeignKey(Course)
    
# class StudentAssignedToExamCenter(models.Model):
#     student = models.ForeignKey(StudentProfile)
#     examCenter = models.ForeignKey(ExamCenter)
    
# class CourseAssessedByTest(models.Model):
#     test = models.ForeignKey(Test)
#     course = models.ForeignKey(Course)

# class StaffTeachingCourse(models.Model):
#     staff = models.ForeignKey(StaffProfile)
#     course = models.ForeignKey(Course)

# class StaffHasAWorkPeriod(models.Model):
#     staff = models.ForeignKey(StaffProfile)
#     workPeriod = models.ForeignKey(WorkPeriod)
    
# class WorkPeriodAssignedToExamCenter(models.Model):
#     examCenter = models.ForeignKey(ExamCenter)
#     workPeriod = models.ForeignKey(WorkPeriod)
    
# class StudentTakingTest(models.Model):
#     test = models.ForeignKey(Test)
#     student = models.ForeignKey(StudentProfile)
#     dateCompleted = models.DateField()

