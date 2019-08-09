#import flask functions
from flask import Flask, render_template
from flask import request
#importing datetime for the date functions
import datetime
#needed for accessing the image files
import os, sys
#needed for reading and writing
import csv
#needed for calculating average reviews
import statistics
#needed for validation
import re

#creating a Flask object
app = Flask(__name__)

#defining globally used variables
errNoUser = ["", ""]
errDate = ""
errPrice = ""
errList = ["", "", "", "", ""]
userInfo = ["", "", "Guest", "", "", "", ""]
filItems = ["", "", "", ""]
today = (datetime.datetime.now()).strftime("%Y-%m-%d")

#a function used for reading a file        
def readFile(aFile):
    #open the file
    with open(aFile, 'r') as inFile:
        #read the file
        reader = csv.reader(inFile)
        #for each row, add the row as an element to the list aList
        aList = [row for row in reader]
    return aList

#a function used for writing the file
def writeFile(aList,aFile):
    #open the file
    with open(aFile, 'w', newline='') as outFile:
        #write the list to the file
        writer = csv.writer(outFile)
        writer.writerows(aList)

#reading all of the needed files
logo = 'static/fish_eagle.jpg'
propFile = 'static/properties.csv'
propList = readFile(propFile)
userFile = 'static/users.csv'
userList = readFile(userFile)
reviewFile = 'static/reviews.csv'
reviewList = readFile(reviewFile)
attracFile = 'static/attractions.csv'
attracList = readFile(attracFile)
bookFile = 'static/bookings.csv'
bookList = readFile(bookFile)

##################################################################Validation################################################################################################
        
#a function to check if a string is blank
def valNotBlank(string):
    errMsg = ""
    #get rid of white space then check the length
    if len((string).replace(" ", "")) == 0:
        #if this length is 0, an error message is set
        errMsg = "Required field is empty."
    return errMsg

#a function for checking if a value is an integer
def valInt(number):
    #try to convert the value to an int
    try:
        #if successful, true is returned
        int(number)
        return True
    #if not successful, false  is returned
    except ValueError:
        return False

#a function for checking if a value is a float
def valFloat(number):
    #try to convert the value to an int
    try:
        #if successful, true is returned
        float(number)
        return True
    #if not successful, false  is returned
    except ValueError:
        return False

#a function for checking if an email is valid
def valEmail(email):
    errMsg = ""
    
    #removes white space and then checks the entered value against this regex expression
    match = re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", email.replace(" ",""))

    #if the value doesn't match the regex, an error message is set
    if match == None:
        errMsg = "Invalid email."
    return errMsg

#a function for checking if a password is strong enough
def valPassword(password):
    errMsg = ""
    
    #checks if the length of the password is less than 8
    length_problem = (len(password) < 8)
    
    #checks if there is a special character in the password
    special_problem = re.search("\W", password) is None
    
    #checks if there is an upper case letter in the password
    upper_problem = re.search("[A-Z]", password) is None
    
    #checks if there is a number in the password
    digit_problem = re.search("[0-9]", password) is None
    
    #checks if there is a lower case letter in the password
    lower_problem = re.search("[a-z]", password) is None
    
    good = not (length_problem or digit_problem or upper_problem or lower_problem or special_problem)
    if good == False:
        #if any of the conditions are not met, an error message is set
        errMsg = "Create a stronger password with lower case letters, upper case letters, numbers and symbols."
    return errMsg

#a function for checking if an area code is valid
def valAreaCode(acode):
    errMsg = ""
    
    #checks to see if the value starts with a '+'
    if acode[0] == "+":
        if len(acode) > 4:
            errMsg = "Invalid area code."
        else:
            #checks if the area code is valid using various conditions
            #if any of the conditions are not met, an error message is set
            if len(acode) == 4:
                if re.search("[1-9]", acode[1]) is None and re.search("[0-9]", acode[2]) is not None and re.search("[0-9]", acode[3]) is not None:
                    errMsg = "Invalid area code."

            elif len(acode) == 3:
                if re.search("[1-9]", acode[1]) is None and re.search("[0-9]", acode[2]) is not None:
                    errMsg = "Invalid area code."

            elif len(acode) == 2:
                if re.search("[1,7]", acode[1]) is None:
                    errMsg = "Invalid area code."
    else:
        errMsg = "Invalid area code."
    return errMsg

#a function for checking a phone number
def valPhoneNo(phone):
    errMsg = ""
    length = len(phone)
    
    #checks to see if the length of the phone number is correct
    if length > 13 or length < 3 or valInt(phone) == False:
        #if not, an error message is set
        errMsg = "Invalid phone number."
    return errMsg

#a function for checking postcodes
def valPostCode(pcode):
    errMsg = ""
    #uses a regex expression to see if the postcode matches the correct format
    if (re.match("^([A-Za-z][A-Ha-hJ-Yj-y]?[0-9][A-Za-z0-9]? [0-9][A-Za-z]{2}|[Gg][Ii][Rr] 0[Aa]{2})$", pcode)) is None:
        #if not, then an error message is set
        errMsg = "Invalid post code."
    return errMsg

#a function to check the desired booking dates are valid
def valBookDate(start, end, bookings):
    errDate = "Your booking was successful."

    #checks to see if the start date is after the end date
    if (start > end):
        errDate = "The start date is after the end date."

    try:
        #checks to see if the desired dates are already booked
        for row in bookings:
            if ((start >= row[3] and start <= row[4]) or (end >= row[3] and end <= row[4]) or (start <= row[3] and end >= row[4])):
                errDate = "Some of these days are already booked."
    except:
        #if not, then an error message is set
        errDate = "Your booking was successful."
    return errDate

###################################################################################################################################################################

#############################################################Homepage Filters######################################################################################

#a function to filter the properties based on price
def filPrice(price1,price2,filList):
    i = 0
    correct = []
    
    #if both filters are blank, return all of the properties
    if price1 == "" and price2 == "":
        return (filList)
    else:
        #if only one is blank, return all of the properties up to the maximum or after the minimum
        if price1 == "":
            price1 = 0
        elif price2 == "":
            price2 = 9e99
        for list in filList:
            #else return the properties that are after the minimum and before the maximim
            if float(filList[i][5]) <= float(price2) and float(filList[i][5]) >= float(price1):
                correct.append(filList[i])
            i += 1
        return (correct)

#a function to filter the properties based on the minimum rating
def filRating(minRate,filList):
    i = 0
    correct = []
    
    #if the filter is left blank, return all the properties
    if minRate == "":
        return (filList)
    else:
        for list in filList:
            #if the property rating is above the minimum, it is returned
            if float(filList[i][6]) >= float(minRate):
                correct.append(filList[i])
            i += 1
        return (correct)

#a function to filter the properties based on the country it is located in
def filCountry(country,filList):
    i = 0
    correct = []
    
    #if the filter is blank, return all of the properties
    if country == "":
        return (filList)
    else:
        for list in filList:
            #if the property location matches the desired locaiton, it is returned
            if (filList[i][4]).lower() == country.lower():
                correct.append(filList[i])
            i += 1
        return (correct)

###################################################################################################################################################################

###########################################################Admin Page Filters######################################################################################

#a function to filter bookings based on the property name
def filProp(pName,filList):
    i = 0
    correct = []

    #if the filter is blank, return all of the bookings
    if pName == "":
        return (filList)
    else:
        for list in filList:
            #if the property name of the booking matches the desired property name, it is returned
            if filList[i][1] == pName:
                correct.append(filList[i])
            i += 1
        return (correct)

#a function to filter bookings based on the time period
def filBPeriod(bPeriod,filList):
    i = 0
    correct = []
    now = (datetime.datetime.now()).date()

    #if the desired time period is in the past, return bookings whose departure date is before now
    if bPeriod == "past":
        for list in filList:
            depDate = (datetime.datetime.strptime(filList[i][4], "%d/%m/%Y")).date()
            if depDate < now:
                correct.append(filList[i])
            i += 1
        return (correct)
    
    #if the desired time period is for current bookings, return bookings whose departure date is after now
    elif bPeriod == "curr":
        for list in filList:
            depDate = (datetime.datetime.strptime(filList[i][4], "%d/%m/%Y")).date()
            if depDate >= now:
                correct.append(filList[i])
            i += 1
        return (correct)

    #otherwise, return all bookings
    else:
        return (filList)

#a function to filter bookings based on the their confirmation
def filBConf(bConf,filList):
    i = 0
    correct = []

    #if the desired booking status is yes, returns bookings whose confirmation status is yes
    if bConf == "conf":
        for list in filList:
            if filList[i][6] == "Yes":
                correct.append(filList[i])
            i += 1
        return (correct)
    
    #if the desired booking status is no, returns bookings whose confirmation status is no
    elif bConf == "unconf":
        for list in filList:
            if filList[i][6] == "No":
                correct.append(filList[i])
            i += 1
        return (correct)
    
    #otherwise, return all bookings
    else:
        return (filList)

###################################################################################################################################################################

#########################################################Space Saving##############################################################################################

def bookA():
    #reads bookList and sets bookRestore as bookList
    bookList = readFile(bookFile)
    bookRestore = bookList
    
    bookAdmin = []
    #adds the contents of bookList to bookAdmin
    for row in bookList:                                                                                                
        bookAdmin.append(row)
    try:
        for book in bookAdmin:                                                                                             
            #converts the dates in bookAdmin into a more consistent format                                                                                                                                                          
            book[3] = datetime.datetime.strftime(datetime.datetime.strptime(book[3], "%Y-%m-%d"), "%d/%m/%Y")           
            book[4] = datetime.datetime.strftime(datetime.datetime.strptime(book[4], "%Y-%m-%d"), "%d/%m/%Y")
    except:
        bookAdmin = []
    
    #restores the new bookList
    bookList = bookRestore
    
    return bookAdmin

def userI():
    #returns the user info found using their email, which either they enter, or is passed from a previous web page
    uEmail = request.form[('uEmail')]
    userInfo = ["", "", "Guest", "", "", "", ""]                                                                         
    for row in userList:                                                                                                 
        if row[0] == uEmail:                                                                                             
            userInfo = row                                                                                               
    return userInfo

def bookL():
    #creates a list of the bookings for the property, excluding those that have finished
    propName = request.form[('propName')]
    bookings = []
    bookList = readFile(bookFile)
    try:
        for row in bookList:
            if row[1] == propName and row[4] >= today:
                bookings.append(row)
    except:
        bookings = []
    return bookings

def revs():
    #creates a list of the reviews for the property
    propName = request.form[('propName')]
    reviews = []                                                                            
    for row in reviewList:                                                                  
        try:                                                                                
            if row[0] == propName:                                                  
                reviews.append(row)
        except:                                                                             
            reviews = []
    return reviews

def revsFirst(reviews):
    revBttn = False
    firstRevs = []
    
    #counts the number of reviews and creates a message if there are too many
    if(len(reviews) > 3):
        for i in range(0,3):
            firstRevs.append(reviews[i])
        revBttn = True
    return firstRevs, revBttn

def propI():
    propName = request.form[('propName')]

    #sets propRestore as propList
    propList = readFile(propFile)
    propRestore = propList
    
    for row in propList:                                                                                                    
        if row[0] == propName:
            #formats price to 2dp and ratings to 1dp for the row passed to the html
            row[5] = '{:,.2f}'.format(float(row[5]))
            if row[6] != "":
                row[6] = '{:.1f}'.format(float(row[6]))

            #finds the images relating to a property and adds the names of these images to the list pImgs
            imgFldr = os.listdir('static/gallery/' + row[0])
            imgs = ['gallery/' + row[0] + '/' + file for file in imgFldr]
            row.append(imgs)

            propInfo = row

    #restores the new PropList
    propList = propRestore
    
    return propInfo

###################################################################################################################################################################

####################################################################Additional Functions###########################################################################

#used for working out the position of the dates as days of the year
def dayCalc(bookList):
    dayList = ""
    try:
        for row in bookList:
            #start and end date are converted into date format
            start = datetime.datetime.strptime(row[3], "%Y-%m-%d").date()
            end = datetime.datetime.strptime(row[4], "%Y-%m-%d").date()
            
            #get the year
            year = 2018
            
            #get the start of the year
            time = datetime.date(year, 1, 1)
            
            #number of days between the start date and the end date
            number = end - start
            
            #for this number of days
            for i in range(0,number.days):
                #position of the day from the start of the year
                day = (start - time)
                
                #increment by one for the number of days
                num = ((day.days) + i)

                #add them to the dayList variable with a ! at the end used for seperating them again later
                dayList = dayList + str(num) + "!"
        #returns the list of days
        return(dayList)
        #E.G. booking from the 5th Jan to the 10th would return 5!6!7!8!9!10!
    except:
        return(dayList)

#a function to count the number of reviews of a certain number e.g. the number of 1 point reviews etc.
def reviewCount(reviews):
    revCount = ["", "", "", "", ""]
  
    for k in range(1,6):
        i = k
        j = 0
        for row in reviews:
        #counts the reviews if they match the current value of i
            if row[3] != "":
                if float(row[3]) == float(i):
                    #increments the value of j if a match is found
                    j += 1
                    
                    #puts the value of j into the correct position in revCount e.g. the number of 1 star reviews in the first position
                    revCount[i-1] = j
    return revCount

###################################################################################################################################################################

##################################################################Homepage Functions###############################################################################

#a function to render the home page
@app.route('/')
def home():
    return render_template('home.html', logo = logo, propList = propList, filItems = filItems, userInfo = userInfo, errPrice = errPrice)

#a function to render the home page from another page
@app.route('/toHome', methods=['POST'])
def toHome():
    userInfo = userI()
    return render_template('home.html', logo = logo, propList = propList, filItems = filItems, userInfo = userInfo, errPrice = errPrice)

#a function to re-render the homepage when the filters are used
@app.route('/homeFil', methods=['POST'])
def homeFil():
    errPrice = ""
    fil1 = ""
    
    userInfo = userI()
    
    #gets the users input for the price filter
    lowPrice = request.form[('lowPrice')]
    highPrice = request.form[('highPrice')]

    #checks to see if a string was entered as a value for either high price or low price
    if valFloat(lowPrice) == False and lowPrice != "":
        lowPrice = ""
        errPrice = "Only enter a number for the maximum and minimum prices."
    if valFloat(highPrice) == False and highPrice != "":
        highPrice = ""
        errPrice = "Only enter a number for the maximum and minimum prices."

    #checks to see if low price is greater than high price
    if errPrice == "" and highPrice != "":
        if lowPrice > highPrice:
            errPrice = "You entered a maximum price that is less than the minimum price."
            fil1 = propList
        else:
            fil1 = filPrice(lowPrice,highPrice,propList)
    #if no problems are found then the filter function is run
    else:
        fil1 = filPrice(lowPrice,highPrice,propList)

    #gets the users input from the rating and country filters        
    rating = request.form[('rating')]
    country = request.form[('country')]

    filItems = [lowPrice, highPrice, rating, country]

    #runs the filter functions for rating and country
    fil2 = filRating(rating,fil1)
    fil3 = filCountry(country,fil2)

    return render_template('home.html', logo = logo, propList = fil3, filItems = filItems, userInfo = userInfo, errPrice = errPrice)

###################################################################################################################################################################

#################################################################Sign In/Out Functions#############################################################################

#a function to render the sign in page
@app.route('/toSignIn', methods=['POST'])
def signIn():
    errNotUser = ""
    return render_template('signIn.html', logo = logo, userInfo = userInfo, errNotUser = errNotUser)

#a function to re-render the home page after signing out
@app.route('/signOut', methods=['POST'])
def signOut():
    return render_template('home.html', logo = logo, propList = propList, filItems = filItems, userInfo = userInfo)

#a function to check that the user is saved in the system
@app.route('/checkUser', methods = ['POST'])
def checkUser():
    errNotUser = ""
                          
    #gets the user's entry for their email and password
    uEmail = request.form[('email')]
    uPassword = request.form[('password')]

    #checks if the information the user provided is in the system
    userInfo = ["", "", "Guest", "", "", "", ""]
    for row in userList:
        if uEmail == row[0] and uPassword == row[1]:
            userInfo = row
            return render_template('home.html', logo = logo, propList = propList, userInfo = userInfo, filItems = filItems, errNotUser = errNotUser)

    #sets an error message if the user cannot be found
    errNotUser = "Email or password entered was incorrect. Please try again."

    return render_template('signIn.html', logo = logo, errNotUser = errNotUser)

###################################################################################################################################################################

#################################################################Registration Page Functions#######################################################################

#a function to render the registration page
@app.route('/toReg', methods=['POST'])
def toReg():
    errOldEmail = ""
    errDiffPass = ""
    newUser = ["", "", "", "", "+44", "", ""]
    return render_template('register.html', logo = logo, errList = errList, newUser = newUser, errDiffPass = errDiffPass, errOldEmail = errOldEmail, userInfo = userInfo)

#a function to add a user to the system
@app.route('/addUser', methods=['POST'])
def addUser():
    #gets the user's inputs and validates them
    uEmail = request.form[('email')]
    errEmail = valEmail(uEmail)
    uPassword = request.form[('password')]
    errPassword = valPassword(uPassword)
    uConPassword = request.form[('conPassword')]
    uFName = request.form[('fName')]
    uLName = request.form[('lName')]
    uAreaCode = request.form[('areaCode')]

    #as area code and phone number are not required fields they are only validated if not blank
    if valNotBlank(uAreaCode) != "":
        errAreaCode = ""
    else:
        errAreaCode = valAreaCode(uAreaCode)
        
    uPhoneNo = request.form[('phoneNo')]
    if valNotBlank(uPhoneNo) != "":
        errPhoneNo = ""
    else:
        errPhoneNo = valPhoneNo(uPhoneNo)
        
    uPostCode = request.form[('postCode')]
    if valNotBlank(uPostCode) != "":
        errPostCode = ""
    else:
        errPostCode = valPostCode(uPostCode)

    if uAreaCode == "" or uPhoneNo == "":
        uAreaCode = ""
        uPhoneNo = ""
    
    errOldEmail = ""
    errDiffPass = ""
    errList = [errEmail, errPassword, errAreaCode, errPhoneNo, errPostCode]
    newUser = [uEmail, uPassword, uFName, uLName, uAreaCode, uPhoneNo, uPostCode]
                          
    #if no errors are found, the email is checked to see if it is already in the system
    if uPassword == uConPassword and errEmail == "" and errPassword == "" and errAreaCode == "" and errPhoneNo == "" and errPostCode == "":
        for row in userList:
            if row[0] == uEmail:
                errOldEmail = "Email already exists."
                return render_template('register.html', logo = logo, errList = errList, newUser = newUser, errDiffPass = errDiffPass, errOldEmail = errOldEmail, userInfo = userInfo)

        #if everything is fine, then the user's details are added to the system    
        userList.append(newUser)
        writeFile(userList, userFile)

        return render_template('signIn.html', logo = logo)
    else:
        #an error is set if the password and confirmation password do not match
        if uPassword != uConPassword:
            errDiffPass = "The passwords do not match."
        return render_template('register.html', logo = logo, errList = errList, newUser = newUser, errDiffPass = errDiffPass, errOldEmail = errOldEmail, userInfo = userInfo)

###################################################################################################################################################################

#################################################################Admin Page Functions##############################################################################

#a function to render the admin page
@app.route('/toAdmin', methods=['POST'])
def toAdmin():
    userInfo = userI()
    bookAdmin = bookA()
    return render_template('admin.html', logo = logo, userInfo = userInfo, bookAdmin = bookAdmin, propList = propList)

#a function to allow the admin to confirm/unconfirm bookings
@app.route('/confirm', methods=['POST'])
def confirm():
    userInfo = userI()

    #changes the value of the confirmed field from yes to no or no to yes for the corresponding bookId
    bookList = readFile(bookFile)
    bookId = request.form[('bookId')]
    for row in bookList:
        if row[0] == bookId:
            if row[6] == "No":
                row[6] = "Yes"
            else:
                row[6] = "No"
    writeFile(bookList, bookFile)

    bookAdmin = bookA()

    return render_template('admin.html', logo = logo, userInfo = userInfo, bookAdmin = bookAdmin, propList = propList)    

#a function to allow the admins to delete bookings
@app.route('/delete', methods=['POST'])
def delete():
    userInfo = userI()

    #removes the entry in bookList corresponding to the bookId
    bookList = readFile(bookFile)
    bookId = request.form[('bookId')]
    for row in bookList:
        if row[0] == bookId:
            bookList.remove(row)
    writeFile(bookList, bookFile)

    bookAdmin = bookA()

    return render_template('admin.html', logo = logo, userInfo = userInfo, bookAdmin = bookAdmin, propList = propList)

#a function to re-render the admin page when the filters are used
@app.route('/adminFil', methods=['POST'])
def adminFil():
    #gets user input for the admin filter
    propName = request.form[('propName')]
    bookPeriod = request.form[('bookPeriod')]
    bookConf = request.form[('bookConf')]

    userInfo = userI()
    bookAdmin = bookA()

    #runs the filters for property name, time period and confirmation of bookings
    adFil1 = filProp(propName,bookAdmin)
    adFil2 = filBPeriod(bookPeriod,adFil1)
    adFil3 = filBConf(bookConf,adFil2)

    return render_template('admin.html', logo = logo, userInfo = userInfo, bookAdmin = adFil3, propList = propList)

###################################################################################################################################################################

################################################################Property Page Functions############################################################################

#a function to render the property page
@app.route('/toProp', methods=['POST'])
def toProp():
    userInfo = userI()
    propInfo = propI()
    
    #checks to see if the user is signed in
    errNoUser = ["", ""]
    if userInfo[0] == "":
        errNoUser = ["You need to be signed in from the homepage to make a booking.", "You need to be signed in from the homepage to submit a review."]

    #gets the breakdown of the reviews e.g. how many 1 point reviews there are 
    reviews = revs()
    revCount = reviewCount(reviews)
    firstRevs, revBttn = revsFirst(reviews)
        
    bookings = bookL()

    #calculates the number of days within each of the bookings for those that are confirmed
    confBooks = filBConf("conf",bookings)
    confDayList = dayCalc(confBooks)
    if confDayList == "":
        confDayList = "d"

    #calculates the number of days within each of the bookings for those that are unconfirmed
    unconfBooks = filBConf("unconf",bookings)
    unconfDayList = dayCalc(unconfBooks)
    if unconfDayList == "":
        unconfDayList = "d"

    return render_template('prop.html', logo = logo, today = today, propInfo = propInfo, userInfo = userInfo, reviews = reviews, revCount = revCount, firstRevs = firstRevs, revBttn = revBttn, errDate = errDate, errNoUser = errNoUser, bookList = bookList, dayList1 = confDayList, dayList2 = unconfDayList)

#a function to add a booking
@app.route('/addBook', methods=['POST'])
def addBook():
    #gets the data entered by the user
    startDate = request.form[('start')]
    endDate = request.form[('end')]

    userInfo = userI()
    propInfo = propI()
    
    bookings = bookL()
    if bookings is None:
        bookings = []

    #checks to see that the entered dates are valid
    errDate = valBookDate(startDate, endDate, bookings)
    
    #if the dates are valid then the booking is given a bookId and is added to the list of bookings
    if errDate == "" or errDate == "Your booking was successful.":
        if len(bookList) > 0:
            i = len(bookList) - 1
            bookId = int(bookList[i][0]) + 1
            bookings = bookList
        else:
            bookId = 1

        #calculates the total price of the booking
        days = (datetime.datetime.strptime(endDate, "%Y-%m-%d") - datetime.datetime.strptime(startDate, "%Y-%m-%d")).days
        price = '{:,.2f}'.format(days * float(propInfo[5]))
        confirm = "No"
        
        #creates a new booking and adds it to the file
        newBook = [bookId, propInfo[0], userInfo[0], startDate, endDate, price, confirm]
        bookList.append(newBook)
        writeFile(bookList, bookFile)

    bookings = bookL()

    #calculates the number of days within each of the bookings for those that are confirmed
    confBooks = filBConf("conf",bookings)
    confDayList = dayCalc(confBooks)
    if confDayList == "":
        confDayList = "d"

    #calculates the number of days within each of the bookings for those that are unconfirmed
    unconfBooks = filBConf("unconf",bookings)
    unconfDayList = dayCalc(unconfBooks)
    if unconfDayList == "":
        unconfDayList = "d"

    reviews = revs()
    revCount = reviewCount(reviews)
    firstRevs, revBttn = revsFirst(reviews)

    return render_template('prop.html', logo = logo, today = today, propInfo = propInfo, userInfo = userInfo, reviews = reviews, revCount = revCount, firstRevs = firstRevs, revBttn = revBttn, errDate = errDate, errNoUser = errNoUser, bookList = bookList, dayList1 = confDayList, dayList2 = unconfDayList)

#a function to allow the user to add a review
@app.route('/addReview', methods=['POST'])
def addReview():
    #gets the data entered by the user and the property name
    propName = request.form[('propName')]
    comment = request.form[('comment')]
    rating = request.form[('rating')]

    userInfo = userI()
    
    #finds the current time and date
    now = (datetime.datetime.now()).strftime("%d/%m/%Y %H:%M:%S")
    
    #creates the new review entry and adds this  to the reviewFile
    newEntry = [propName, userInfo[0], comment, rating, now]

    reviewList.append(newEntry)
    writeFile(reviewList,reviewFile)

    reviews = revs()
    revCount = reviewCount(reviews)
    firstRevs, revBttn = revsFirst(reviews)

    ratingList = []
    for row in reviews:
        if row[3] != "":
            ratingList.append(float(row[3]))
        
    #calculates the average rating from the reviews of the property
    avgRating = round(statistics.mean(ratingList),1)
    
    #formats the price and rating of the property
    propInfo = []
    for row in propList:
        if row[0] == propName:
            row[5] = '{:,.2f}'.format(float(row[5]))
            row[6] = '{:.1f}'.format(float(avgRating))
            propInfo = row
    writeFile(propList,propFile)

    bookings = bookL()

    #calculates the number of days within each of the bookings for those that are confirmed
    confBooks = filBConf("conf",bookings)
    confDayList = dayCalc(confBooks)
    if confDayList == "":
        confDayList = "d"

    #calculates the number of days within each of the bookings for those that are unconfirmed
    unconfBooks = filBConf("unconf",bookings)
    unconfDayList = dayCalc(unconfBooks)
    if unconfDayList == "":
        unconfDayList = "d"

    return render_template('prop.html', logo = logo, tpday = today, propInfo = propInfo, userInfo = userInfo, reviews = reviews, revCount = revCount, firstRevs = firstRevs, revBttn = revBttn, errNoUser = errNoUser, bookList = bookList, dayList1 = confDayList, dayList2 = unconfDayList)

###################################################################################################################################################################

#################################################################Images Page Functions#############################################################################

#a function to render the images page
@app.route('/toImages', methods=['POST'])
def toImages():
    #gets the information of the property
    propName = request.form[('propName')]
    for row in propList:
        if row[0] == propName:
            propInfo = row
    
    userInfo = userI()
            
    #finds the images relating to the attractions of a property and adds the names of these images to the list attracs
    attracs = []
    for row in attracList:
        if propInfo[7] == row[0]:
            imgFldr = os.listdir('static/gallery/' + row[5])
            imgs = ['gallery/' + row[5] + '/' + file for file in imgFldr]
            attracs.append([row[1], row[2], row[3], row[4], row[5], imgs])
            
    return render_template('images.html', logo = logo, propInfo = propInfo, userInfo = userInfo, attracs = attracs)

###################################################################################################################################################################

#runs the app
if __name__ == '__main__':
    app.run(debug = True)
