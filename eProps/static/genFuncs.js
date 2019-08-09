// home.html functions

//A function show either the sign in or sign out button depending on if the user is signed in or not
function showSign(email) {
	if (email !== "") {
		document.getElementById("signOut").style.display = "block";
	} else {
		document.getElementById("signIn").style.display = "block";
	}
}

//A function to display the admin button if the user is logged in as an admin
function showAdmin(email) {
	if (email == "admin@eprops.co.uk") {
		document.getElementById("admin").style.display = "block";
	}
}


// prop.html functions

//A function to set the flex-grow values of the review section based on variables passed in from the html
function revBar(avg, rev1, rev2, rev3, rev4, rev5) {
	//The green section is the average rating
	document.getElementById("revGreen").style.flexGrow = avg;
	if (avg !== '') {
		//The remainder is red
		document.getElementById("revRed").style.flexGrow = (5 - avg);
	}

	document.getElementById("r1").style.flexGrow = rev1;
	document.getElementById("r2").style.flexGrow = rev2;
	document.getElementById("r3").style.flexGrow = rev3;
	document.getElementById("r4").style.flexGrow = rev4;
	document.getElementById("r5").style.flexGrow = rev5;
}

//A function to hide the add booking and review buttons if the user is not signed in
function showBookRev(email) {
	if (email === "") {
		document.getElementById("addBook").style.display = "none";
		document.getElementById("addReview").style.display = "none";
	}
}

//A function to display a message depending on whether or not the booking was successful
function showAlert(errDate) {
	if (errDate == "Your booking was successful.") {
		document.getElementById("al").style.display = "block";
		document.getElementById("al").style.backgroundColor = "#00f300";
	} else if (errDate !== "") {
		document.getElementById("al").style.display = "block";
	}
}

//A function display the correct number of reviews
function hideRevs(test) {
	//If there are more than 3 reviews then only the first 3 are displayed
	if (test == "True") {
		document.getElementById("allRevs").style.display = "none";
	}
	//Otherwise they are all displayed
	else {
		document.getElementById("firstRevs").style.display = "none";
	}
}

//Another function to display the correct number of reviews
function showRevs(test) {
	//If there are more than 3 reviews then all of the reviews are displayed
	if (test == "True") {
		document.getElementById("allRevs").style.display = "block";
		document.getElementById("firstRevs").style.display = "none";
	}
}

//A function to work out and display the total cost of the holiday
function totalPrice() {
	//Gets the needed information from the html
	var price = document.getElementById("calendar").getAttribute("data-item");
	var start = new Date(document.getElementById("s").value);
	var end = new Date(document.getElementById("e").value);
	//The difference in the start date and end date is given in milliseconds so it is converted to days
	var difference = ((end - start) / (1000 * 60 * 60 * 24));
	//Works out the total for the number of days selected
	var total = (price * difference);
	//A function to convert the value of total into a currency value
	function format1(n, currency) {
		//replaces the . with commas in the needed positions
		return currency + n.toFixed(2).replace(/./g, function(c, i, a) {
			//Finds where the commas are needed 
			return i > 0 && c !== "." && (a.length - i) % 3 === 0 ? "," + c : c;
		});
	}
	//If dates are correctly entered the result will not be a NaN so the price is displayed in currency format
	if(isNaN(total) == false){
		document.getElementById("totalPrice").innerHTML = "Your total price is: " + format1(total, "£");
	}
	//Otherwise there must have been an error so a message is displaying telling the user something went wrong
	else{
		document.getElementById("totalPrice").innerHTML = "Your arrival and departure dates must be chosen before the total price can be displayed.";
	}
}

//Works out the number of days in a given month
function daysInMonth(month, year) {
	return new Date(year, month, 0).getDate();
}

//Finds the number of days in between 2 dates
function dateDiff(first, second) {
	return Math.round((second - first) / (1000 * 60 * 60 * 24));
}

//A function to draw the calender for the next year. Adds one to the value of the year and then re-draws the calender
function nextYear() {
	year += 1;
	for (var j = 0; j < 12; j += 1) {
		document.getElementById("CAL" + j).innerHTML = (display(year, j));
	}
}

//A function to draw the calender for the previous year. Subtracts one from the value of the year and then re-draws the calender
function prevYear() {
	year -= 1;
	for (var j = 0; j < 12; j += 1) {
		document.getElementById("CAL" + j).innerHTML = (display(year, j));
	}
}

//A function to set the expanded image to the one that was selected 
function openImg(imgs) {
	var expandImg = document.getElementById("expandedImg");
	expandImg.src = imgs.src;
}


// admin.html functions

//A function to show the home button on the admin page
function showHome(email) {
	if (email == "admin@eprops.co.uk") {
		document.getElementById("home").style.display = "block";
	}
}