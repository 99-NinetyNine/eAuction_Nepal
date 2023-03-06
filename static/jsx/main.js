(function ($) {
    "user strict";
    // Preloader Js
    $(window).on('load', function () {
        $('#overlayer').fadeOut(1000);
        var img = $('.bg_img');
        img.css('background-image', function () {
            var bg = ('url(' + $(this).data('background') + ')');
            return bg;
        });
        galleryMasonary();
        galleryMasonaryTwo();
    });
    // play
    function galleryMasonary() {
        // filter functions
        var $grid = $(".auction-wrapper-5");
        var filterFns = {};
        $grid.isotope({
            itemSelector: '.auction-item-5',
            masonry: {
                columnWidth: 0,
            }
        });
        // bind filter button click
        $('ul.filter').on('click', 'li', function () {
            var filterValue = $(this).attr('data-check');
            // use filterFn if matches value
            filterValue = filterFns[filterValue] || filterValue;
            $grid.isotope({
                filter: filterValue
            });
        });
        // change is-checked class on buttons
        $('ul.filter').each(function (i, buttonGroup) {
            var $buttonGroup = $(buttonGroup);
            $buttonGroup.on('click', 'li', function () {
                $buttonGroup.find('.active').removeClass('active');
                $(this).addClass('active');
            });
        });
    }
    // Gallery Masonary
    function galleryMasonaryTwo() {
        // filter functions
        var $gridTwo = $(".auction-wrapper-7");
        var filter = {};
        $gridTwo.isotope({
            itemSelector: '.auction-item-7',
            masonry: {
                columnWidth: 0,
            }
        });
        // bind filter button click
        $('ul.filter').on('click', 'li', function () {
            var filterValueTwo = $(this).attr('data-check');
            // use filterFn if matches value
            filterValueTwo = filter[filterValueTwo] || filterValueTwo;
            $gridTwo.isotope({
                filter: filterValueTwo
            });
        });
        // change is-checked class on buttons
        $('ul.filter').each(function (i, buttonGroup) {
            var $buttonGroupTwo = $(buttonGroup);
            $buttonGroupTwo.on('click', 'li', function () {
                $buttonGroupTwo.find('.active').removeClass('active');
                $(this).addClass('active');
            });
        });
    }
    $(document).ready(function () {
        //Bidding All Events Here
        //New Countdown Starts
        if ($("#bid_counter1").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter1");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter2").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter2");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter3").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter3");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter4").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter4");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter5").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter5");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter6").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter6");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter7").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter7");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter8").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter8");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter9").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter9");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter10").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter10");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter11").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter11");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter12").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter12");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter13").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter13");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter14").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter14");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter15").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter15");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter16").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter16");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter17").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter17");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter18").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter18");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter19").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter19");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter20").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter20");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter21").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter21");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter22").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter22");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter23").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter23");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter24").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter24");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter25").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter25");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter26").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter26");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter27").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter27");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter28").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter28");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter29").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter29");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter30").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter30");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter31").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter31");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter32").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter32");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter33").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter33");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#bid_counter34").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#bid_counter34");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d  : ";
                    message += re_hours + "h  : ";
                    message += remaining.minutes + "m  : ";
                    message += remaining.seconds + "s";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#min_counter_1").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#min_counter_1");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d ";
                    message += re_hours + "h ";
                    message += remaining.minutes + "m";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#min_counter_1").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#min_counter_2");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d ";
                    message += re_hours + "h ";
                    message += remaining.minutes + "m";
                }
                counterElement.textContent = message;
            });
        }
        //New Countdown Starts
        if ($("#min_counter_1").length) {
            // If you need specific date then comment out 1 and comment in 2
            // let endDate = "2020/03/20"; //This is 1
            let endDate = (new Date().getFullYear()) + '/' + (new Date().getMonth() + 1) + '/' + (new Date().getDate() + 1); //This is 2
            let counterElement = document.querySelector("#min_counter_3");
            let myCountDown = new ysCountDown(endDate, function (remaining, finished) {
                let message = "";
                if (finished) {
                    message = "Expired";
                } else {
                    var re_days = remaining.totalDays;
                    var re_hours = remaining.hours;
                    message += re_days + "d ";
                    message += re_hours + "h ";
                    message += remaining.minutes + "m";
                }
                counterElement.textContent = message;
            });
        }
        // Nice Select
        $('.select-bar').niceSelect();
        // counter 
        $('.counter').countUp({
            'time': 2500,
            'delay': 10
        });
        // PoPuP 
        $('.popup').magnificPopup({
            disableOn: 700,
            type: 'iframe',
            mainClass: 'mfp-fade',
            removalDelay: 160,
            preloader: false,
            fixedContentPos: false,
            disableOn: 300
        });
        $("body").each(function () {
            $(this).find(".img-pop").magnificPopup({
                type: "image",
                gallery: {
                    enabled: true
                }
            });
        })
        //Faq
        $('.faq-wrapper .faq-title').on('click', function (e) {
            var element = $(this).parent('.faq-item');
            if (element.hasClass('open')) {
                element.removeClass('open');
                element.find('.faq-content').removeClass('open');
                element.find('.faq-content').slideUp(300, "swing");
            } else {
                element.addClass('open');
                element.children('.faq-content').slideDown(300, "swing");
                element.siblings('.faq-item').children('.faq-content').slideUp(300, "swing");
                element.siblings('.faq-item').removeClass('open');
                element.siblings('.faq-item').find('.faq-title').removeClass('open');
                element.siblings('.faq-item').find('.faq-content').slideUp(300, "swing");
            }
        });
        //Menu Dropdown Icon Adding
        $("ul>li>.submenu").parent("li").addClass("menu-item-has-children");
        // drop down menu width overflow problem fix
        $('.submenu').parent('li').hover(function () {
            var menu = $(this).find("ul");
            var menupos = $(menu).offset();
            if (menupos.left + menu.width() > $(window).width()) {
                var newpos = -$(menu).width();
                menu.css({
                    left: newpos
                });
            }
        });
        $('.menu li a').on('click', function (e) {
            var element = $(this).parent('li');
            if (element.hasClass('open')) {
                element.removeClass('open');
                element.find('li').removeClass('open');
                element.find('ul').slideUp(300, "swing");
            } else {
                element.addClass('open');
                element.children('ul').slideDown(300, "swing");
                element.siblings('li').children('ul').slideUp(300, "swing");
                element.siblings('li').removeClass('open');
                element.siblings('li').find('li').removeClass('open');
                element.siblings('li').find('ul').slideUp(300, "swing");
            }
        })
        // Scroll To Top 
        var scrollTop = $(".scrollToTop");
        $(window).on('scroll', function () {
            if ($(this).scrollTop() < 500) {
                scrollTop.removeClass("active");
            } else {
                scrollTop.addClass("active");
            }
        });
        //Click event to scroll to top
        $('.scrollToTop').on('click', function () {
            $('html, body').animate({
                scrollTop: 0
            }, 500);
            return false;
        });
        //Header Bar
        $('.header-bar').on('click', function () {
            $(this).toggleClass('active');
            $('.overlay').toggleClass('active');
            $('.menu').toggleClass('active');
        })
        $('.overlay').on('click', function () {
            $(this).removeClass('active');
            $('.header-bar').removeClass('active');
            $('.menu').removeClass('active');
            $('.cart-sidebar-area').removeClass('active');
        })
        $('.cart-button, .side-sidebar-close-btn').on('click', function () {
            $(this).toggleClass('active');
            $('.overlay').toggleClass('active');
            $('.cart-sidebar-area').toggleClass('active');
        })
        $('.search-bar').on('click', function () {
            $('.search-form').toggleClass('active');
        })
        $('.remove-cart').on('click', function (e) {
            e.preventDefault();
            $(this).parent().parent().hide(300);
        });
        // Header Sticky Herevar prevScrollpos = window.pageYOffset;
        var scrollPosition = window.scrollY;
        if (scrollPosition >= 1) {
            $(".header-section").addClass('active');
        }
        var header = $(".header-bottom");
        $(window).on('scroll', function () {
            if ($(this).scrollTop() < 1) {
                header.removeClass("active");
            } else {
                header.addClass("active");
            }
        });
        $('.tab ul.tab-menu li').on('click', function (g) {
            var tab = $(this).closest('.tab'),
                index = $(this).closest('li').index();
            tab.find('li').siblings('li').removeClass('active');
            $(this).closest('li').addClass('active');
            tab.find('.tab-area').find('div.tab-item').not('div.tab-item:eq(' + index + ')').hide(10);
            tab.find('.tab-area').find('div.tab-item:eq(' + index + ')').fadeIn(10);
            g.preventDefault();
        });
        //Client Slider
        $('.client-slider').owlCarousel({
            loop: true,
            responsiveClass: true,
            nav: false,
            dots: false,
            loop: true,
            autoplay: true,
            autoplayTimeout: 2000,
            autoplayHoverPause: true,
            items: 1,
            autoHeight: true,
            responsive: {
                768: {
                    items: 2,
                },
                992: {
                    items: 3,
                },
                1200: {
                    items: 3,
                },
            }
        })
        //Auction Slider One
        $('.auction-slider-1').owlCarousel({
            // loop:true,
            nav: false,
            dots: false,
            items: 1,
            autoplay: true,
            autoplayTimeout: 2500,
            autoplayHoverPause: true,
            autoHeight: true,
            margin: 30,
        });
        var owlOne = $('.auction-slider-1');
        owlOne.owlCarousel();
        // Go to the next item
        $('.electro-next').on('click', function () {
            owlOne.trigger('next.owl.carousel');
        })
        // Go to the previous item
        $('.electro-prev').on('click', function () {
            owlOne.trigger('prev.owl.carousel', [300]);
        })
        //Auction Slider
        $('.auction-slider-2').owlCarousel({
            // loop:true,
            nav: false,
            dots: false,
            items: 1,
            autoplay: true,
            autoplayTimeout: 2500,
            autoplayHoverPause: true,
            autoHeight: true,
            margin: 30,
        });
        var owlTwo = $('.auction-slider-2');
        owlTwo.owlCarousel();
        // Go to the next item
        $('.art-next').on('click', function () {
            owlTwo.trigger('next.owl.carousel');
        })
        // Go to the next item
        $('.art-prev').on('click', function () {
            owlTwo.trigger('prev.owl.carousel');
        })
        //Browse Auction Slider
        $('.browse-slider').owlCarousel({
            loop: true,
            nav: false,
            dots: false,
            items: 1,
            autoplay: true,
            autoplayTimeout: 2500,
            autoplayHoverPause: true,
            autoHeight: true,
            responsive: {
                450: {
                    items: 2,
                },
                768: {
                    items: 3,
                },
                992: {
                    items: 5,
                },
                1200: {
                    items: 6,
                },
            }
        });
        var owlThree = $('.browse-slider');
        owlThree.owlCarousel();
        // Go to the next item
        $('.bro-next').on('click', function () {
            owlThree.trigger('next.owl.carousel');
        })
        // Go to the previous item
        $('.bro-prev').on('click', function () {
            owlThree.trigger('prev.owl.carousel', [300]);
        })
        //Browse Auction Slider
        $('.browse-slider-2').owlCarousel({
            loop: true,
            nav: false,
            dots: false,
            items: 1,
            autoplay: true,
            autoplayTimeout: 2500,
            autoplayHoverPause: true,
            autoHeight: true,
            responsive: {
                500: {
                    items: 2,
                },
                992: {
                    items: 3,
                },
                1200: {
                    items: 4,
                },
            }
        });
        var owlBrowseTwo = $('.browse-slider-2');
        owlBrowseTwo.owlCarousel();
        // Go to the next item
        $('.bro-next').on('click', function () {
            owlBrowseTwo.trigger('next.owl.carousel');
        })
        // Go to the previous item
        $('.bro-prev').on('click', function () {
            owlBrowseTwo.trigger('prev.owl.carousel', [300]);
        })
        //Browse Auction Slider
        $('.auction-slider-4').owlCarousel({
            // loop: true,
            nav: false,
            dots: true,
            items: 1,
            autoplay: true,
            autoplayTimeout: 2500,
            autoplayHoverPause: true,
            autoHeight: true,
            margin: 30,
            responsive: {
                768: {
                    items: 2,
                },
                992: {
                    items: 1,
                },
            }
        });
        var owlFour = $('.auction-slider-4');
        owlFour.owlCarousel();
        // Go to the next item
        $('.real-next').on('click', function () {
            owlFour.trigger('next.owl.carousel');
        })
        // Go to the previous item
        $('.real-prev').on('click', function () {
            owlFour.trigger('prev.owl.carousel', [300]);
        })
        //The Password Show
        $('.pass-type').on('click', function () {
            var x = document.getElementById("login-pass");
            if (x.type === "password") {
                x.type = "text";
            } else {
                x.type = "password";
            }
        });
        $(function () {
            $("#slider-range").slider({
                range: true,
                min: 0,
                max: 10000,
                values: [600, 7000],
                slide: function (event, ui) {
                    $("#amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
                }
            });
            $("#amount").val("$" + $("#slider-range").slider("values", 0) + " - $" + $("#slider-range").slider("values", 1));
        });
        var sync1 = $("#sync1");
        var sync2 = $("#sync2");
        var thumbnailItemClass = '.owl-item';
        var slides = sync1.owlCarousel({
            startPosition: 12,
            items: 1,
            loop: true,
            margin: 0,
            mouseDrag: true,
            touchDrag: true,
            pullDrag: false,
            scrollPerPage: true,
            autoplayHoverPause: false,
            nav: false,
            dots: false,
        }).on('changed.owl.carousel', syncPosition);

        function syncPosition(el) {
            $owl_slider = $(this).data('owl.carousel');
            var loop = $owl_slider.options.loop;

            if (loop) {
                var count = el.item.count - 1;
                var current = Math.round(el.item.index - (el.item.count / 2) - .5);
                if (current < 0) {
                    current = count;
                }
                if (current > count) {
                    current = 0;
                }
            } else {
                var current = el.item.index;
            }

            var owl_thumbnail = sync2.data('owl.carousel');
            var itemClass = "." + owl_thumbnail.options.itemClass;

            var thumbnailCurrentItem = sync2
                .find(itemClass)
                .removeClass("synced")
                .eq(current);
            thumbnailCurrentItem.addClass('synced');

            if (!thumbnailCurrentItem.hasClass('active')) {
                var duration = 500;
                sync2.trigger('to.owl.carousel', [current, duration, true]);
            }
        }
        var thumbs = sync2.owlCarousel({
            startPosition: 12,
            items: 2,
            loop: false,
            margin: 0,
            autoplay: false,
            nav: false,
            dots: false,
            responsive: {
                500: {
                    items: 3,
                },
                768: {
                    items: 4,
                },
                992: {
                    items: 5,
                },
                1200: {
                    items: 6,
                },
            },
            onInitialized: function (e) {
                var thumbnailCurrentItem = $(e.target).find(thumbnailItemClass).eq(this._current);
                thumbnailCurrentItem.addClass('synced');
            },
        })
            .on('click', thumbnailItemClass, function (e) {
                e.preventDefault();
                var duration = 500;
                var itemIndex = $(e.target).parents(thumbnailItemClass).index();
                sync1.trigger('to.owl.carousel', [itemIndex, duration, true]);
            }).on("changed.owl.carousel", function (el) {
                var number = el.item.index;
                $owl_slider = sync1.data('owl.carousel');
                $owl_slider.to(number, 500, true);
            });
        sync1.owlCarousel();
        // Go to the next item
        $('.det-next').on('click', function () {
            sync1.trigger('next.owl.carousel');
            sync2.trigger('next.owl.carousel');
        })
        // Go to the previous item
        $('.det-prev').on('click', function () {
            sync1.trigger('prev.owl.carousel', [300]);
            sync2.trigger('prev.owl.carousel', [300]);
        })
    });
})(jQuery);
