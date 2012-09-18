from django.db import models, transaction
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

#from profiles.models import BaseProfile
from django.contrib.auth.models import User
from profiles.models import prettyNameOfUser

from django.db.models import Q

import datetime
ONE_DAY = datetime.timedelta(days=1)

EXAM_CENTER_RM_100_CAPACITY = 30



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



class Period():
    """Note period starts differently on fridays.
    So these constants should be treated as "code" or "period ID".
    For actual start times, see FRIDAY_PERIOD_STARTS
    and MON_TO_THUR_PERIOD_STARTS."""
    TUTORIAL = 0
    ONE = 1
    TWO = 2
    LUNCH = 3
    THREE = 4
    FOUR = 5
    AFTERSCHOOL = 6
    SCHOOL_CLOSES = 7
    END_OF_DAY = 8
    ID_OF_NEXT = {
        TUTORIAL: ONE,
        ONE: TWO,
        TWO: LUNCH,
        LUNCH: THREE,
        THREE: FOUR,
        FOUR: AFTERSCHOOL,
        AFTERSCHOOL: SCHOOL_CLOSES,
        SCHOOL_CLOSES: END_OF_DAY
        }
    CHOICES = (
        (TUTORIAL, 'Tutorial Time'),
        (ONE, 'Period 1'),
        (TWO, 'Period 2'),
        (LUNCH, 'Lunch Time'),
        (THREE, 'Period 3'),
        (FOUR, 'Period 4'),
        (AFTERSCHOOL, 'After School'),
        )
    TIME_VERBOSE_NAME_MAP = dict(CHOICES)
    
    # this is rather ugly. should've thought of this problem before,
    # where period starts can change whenver for any reason
    # todo: fix this when we rewrite this App as planned
    FRIDAY_PERIOD_START_TIMES = {
        TUTORIAL: 900,
        ONE: 905,
        TWO: 1010,
        LUNCH: 1114,
        THREE: 1115,
        FOUR: 1220,
        AFTERSCHOOL: 1320,
        SCHOOL_CLOSES: 1500,
        END_OF_DAY: 2359
        }
    FRIDAY_PERIOD_START_TIMES_TO_ID = dict((v,k) for k,v in FRIDAY_PERIOD_START_TIMES.iteritems())
    MON_TO_THUR_PERIOD_START_TIMES = {
        TUTORIAL: 830,
        ONE: 855,
        TWO: 1030,
        LUNCH: 1200,
        THREE: 1230,
        FOUR: 1405,
        AFTERSCHOOL: 1535,
        SCHOOL_CLOSES: 1700,
        END_OF_DAY: 2359
        }
    MON_TO_THUR_PERIOD_START_TIMES_TO_ID = dict((v,k) for k,v in MON_TO_THUR_PERIOD_START_TIMES.iteritems())

    @classmethod
    def idOfPeriodStartTimeOnDay(cls, periodStarts, theDay):
        if periodStarts >= cls.TUTORIAL and periodStarts <= cls.END_OF_DAY:
            # we're abusing the database testBeginTime field.
            # testBeginTime model field is hacked to support storing
            # period IDs prior to a call to save(), but should always
            # be set to real period start times when save()ing
            return periodStarts
            # in the short term, this hack should work most of the
            # time without ambiguity since no period actually starts
            # between 00:00 and 00:08. In the long term, this is a
            # todo and should be fixed in the next rewrite.
            
        FRIDAY = 4
        if theDay == datetime.date(2012,12,31):
            # special day, treated specially
            periodIDs = cls.FRIDAY_PERIOD_START_TIMES_TO_ID
        elif theDay.weekday() == FRIDAY:
            periodIDs = cls.FRIDAY_PERIOD_START_TIMES_TO_ID
        else:
            periodIDs = cls.MON_TO_THUR_PERIOD_START_TIMES_TO_ID
        return periodIDs[periodStarts]
    
    @classmethod
    def startTimeOfPeriodIdOnDay(cls, thePeriodId, theDay):
        FRIDAY = 4
        if theDay == datetime.date(2012,12,31):
            # special day, treated specially
            periodStarts = cls.FRIDAY_PERIOD_START_TIMES
        elif theDay.weekday() == FRIDAY:
            periodStarts = cls.FRIDAY_PERIOD_START_TIMES
        else:
            periodStarts = cls.MON_TO_THUR_PERIOD_START_TIMES
        return periodStarts[thePeriodId]

    @classmethod
    def nextPeriodStartTimeOfPeriodIdOnDay(cls, thePeriodId, theDay):
        """ insert period schedule into startsOnDay(...)
        """
        nextPerId = cls.ID_OF_NEXT[thePeriodId]
        return cls.startTimeOfPeriodIdOnDay(nextPerId, theDay)

    @classmethod
    def lengthOfPeriodIdOnDay(cls, periodId, theDay):
        return cls.nextPeriodStartTimeOfPeriodIdOnDay(periodId, theDay) - cls.startTimeOfPeriodIdOnDay(periodId, theDay)


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
    # testDuration = models.CharField(max_length=40,
    #                                 verbose_name="Test Duration")
    testDate = models.DateField(verbose_name="Test on Date")

    # workPeriod = models.ForeignKey(WorkPeriod)
    #testPeriod = models.IntegerField(choices=TEST_PERIOD_CHOICES,
    #                                    default=PERIOD_AFTERSCHOOL,
    #                                    verbose_name="Test in Period")
    testBeginTime = models.IntegerField(verbose_name="Test in Period")
    testEndTime = models.PositiveIntegerField(verbose_name="Test in Period")

    testDuration = models.PositiveIntegerField(verbose_name="Test Duration") # this should be testEndTime - testBeginTime
    # apparently ModelForm cannot add in "virtual" form fields that have no model backing (&*^#^&
    
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
    noShow = models.BooleanField(verbose_name="No Show")

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
                            'testBeginTime',),)

    def __repr__(self):
        s = (self.studentFirstName + " " + self.studentLastName)
        s += (" in " + self.testCourseName + ": ")
        if self.testCompleted:
            done = " is completed on "
        else:
            done = " is NOT completed on "
        s += ("Test " + self.testName + done)
        s += (str(self.testDate) + " " + Period.TIME_VERBOSE_NAME_MAP[self.testBeginTime])

        return s
#        return super(Booking, self).__repr__()

    def __str__(self):
        return self.__repr__()
        
    def clean(self):
        perId = Period.idOfPeriodStartTimeOnDay(self.testBeginTime, self.testDate)
        if Booking.countAppts(self.testDate, perId) >= EXAM_CENTER_RM_100_CAPACITY:
            raise ValidationError(Period.TIME_VERBOSE_NAME_MAP[self.testBeginTime] + ' on ' + str(self.testDate) + ' is full.')

    def save(self):
        """ may throw ValidationError from full_clean
        """
        with transaction.commit_on_success():
            print "doing transaction"
            self.full_clean()
            super(Booking, self).save()

    @classmethod
    def getFieldnamesStdOrder(cls):
        return ["studentFirstName",
                "studentLastName",
                'studentGrade',
                "testCourseName",
                "courseTeacher",
                'testName',
                'testDate',
                "testBeginTime",
                'testDuration',                
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
                'testCompleted',
                'noShow']

    def fieldDataOf(self, fieldNameStr):
        f = self._meta.get_field(fieldNameStr)
        attname = f.get_attname()
        data= {'name': fieldNameStr,
               'attname': attname, # could be different from fieldNameStr, e.g. courseTeacher_id
               'verbose_name': f.verbose_name,
               'help_text': f.help_text,
               'value': eval("self."+attname)}
        if fieldNameStr  == 'courseTeacher':
            data['value'] = prettyNameOfUser(self.courseTeacher) # avoids showing foreign key id
        elif fieldNameStr == 'testBeginTime':
            theDay = self.fieldDataOf('testDate')['value']
            perTimeStart = data['value']
            perId = Period.idOfPeriodStartTimeOnDay(perTimeStart, theDay)
            data['value'] = Period.TIME_VERBOSE_NAME_MAP[perId]
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
                                              'lower_studentLastName': 'lower(studentLastName)'}).order_by('testDate', 'testBeginTime',
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
                                  'duplicateUrl':{'value':reverse('duplicate_booking',
                                                                  kwargs={'pk':booking.pk}),
                                                  'verbose_name': "Duplicate Booking",
                                                  'help_text': '',
                                                  'name': 'duplicateUrl'},
                                  'setCompletedUrl': {'value':reverse('set_booking_completed',
                                                                      kwargs={'pk':booking.pk}),
                                                      'verbose_name': "Test Taken",
                                                      'help_text': '',
                                                      'name': 'setCompletedUrl'},
                                  'setNoShowUrl': {'value':reverse('set_no_show',
                                                                   kwargs={'pk':booking.pk}),
                                                   'verbose_name': "No Show",
                                                   'help_text': '',
                                                   'name': 'setNoShowUrl'},
                                  'deleteUrl': {'value':reverse('delete_booking',
                                                                kwargs={'pk':booking.pk}),
                                                'verbose_name': "Delete Booking",
                                                'help_text': '',
                                                'name': 'deleteUrl'}
                                  }
            bookingObj['data'] = booking.getNormalizedDataOfFields(orderedFields=orderedFields, incl_false_bool_fields=incl_false_bool_fields)
            bookings_list.append(bookingObj)
        return bookings_list

    @classmethod
    def countAppts(cls, aDatetime, aPeriodId):
        """ aPeriodId is Period.ONE, etc.
        """
        aPeriodStart = Period.startTimeOfPeriodIdOnDay(aPeriodId, aDatetime)
        aPeriodEnds = Period.nextPeriodStartTimeOfPeriodIdOnDay(aPeriodId, aDatetime)
        return cls.objects.filter(testDate=aDatetime, testCompleted=False, noShow=False).filter(Q(testBeginTime__gte=aPeriodStart, testBeginTime__lt=aPeriodEnds) | Q(testEndTime__gt=aPeriodStart, testEndTime__lte=aPeriodEnds) | Q(testBeginTime__lt=aPeriodStart, testEndTime__gt=aPeriodEnds)).count()

    @classmethod
    def apptStats(cls, days = 1, showApptsAvailable = False, verbosePeriodName = True):
        """ provide counts of appts in each period in next days
        """
        day = datetime.date.today()
        
        allStats = []
        for x in range(days):
            dayStats = []
            for k,v in Period.CHOICES:
                periodLength = Period.lengthOfPeriodIdOnDay(k, day)
                if periodLength > 5:
                    if showApptsAvailable:
                        apptCnt = EXAM_CENTER_RM_100_CAPACITY - cls.countAppts(day, k)
                    else:
                        apptCnt = cls.countAppts(day, k)
                else:
                    apptCnt = 0
                    # this is a hack so that every day has same
                    # periods, but some periods are 5 or less minutes
                    # long to show the periods aren't actually
                    # real/useful
                if verbosePeriodName:
                    perName = Period.TIME_VERBOSE_NAME_MAP[k]
                else:
                    perName = k
                dayStats.append({'periodName':perName, 'apptCount': apptCnt})
            allStats.append({'date': day, 'stats': dayStats})
            day += ONE_DAY
            
        return allStats
    


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

