
let midpoint_marker;
let infowindow;
let map;

async function init() {
    // Wait for map to be generated
    await customElements.whenDefined('gmp-map');
    // Select map from the gmp-map generated in the html
    map = document.querySelector("gmp-map");
    url = 'https://maps.googleapis.com/maps/api/staticmap?key=YOUR_API_KEY&center=47.65,-122.35&zoom=12&format=png&maptype=roadmap&style=element:geometry%7Ccolor:0x202c3e&style=element:labels.icon%7Cvisibility:off&style=element:labels.text.fill%7Ccolor:0xffffff%7Clightness:20%7Cgamma:0.01%7Cweight:1.39&style=element:labels.text.stroke%7Ccolor:0x000000%7Csaturation:9%7Cvisibility:on%7Cweight:0.96&style=feature:landscape%7Celement:geometry%7Ccolor:0x29446b%7Csaturation:9%7Clightness:30&style=feature:poi%7Celement:geometry%7Csaturation:20&style=feature:poi.park%7Celement:geometry%7Csaturation:-20%7Clightness:20&style=feature:road%7Celement:geometry%7Csaturation:-30%7Clightness:10&style=feature:road%7Celement:geometry.fill%7Ccolor:0x193a55&style=feature:road%7Celement:geometry.stroke%7Csaturation:25%7Clightness:25%7Cweight:0.01&style=feature:water%7Clightness:-20&size=480x360'
  
    map.innerMap.setOptions({ mapTypeControl: false, styles: new google.maps.StyledMapType(url) });

    // Create an infowindow to be filled above a marker when it is created
    infowindow = new google.maps.InfoWindow();
    infowindowContent = document.getElementById("infowindow-content");
    infowindow.setContent(infowindowContent);

    const indexContent = document.getElementById("index-content");
    const placesContent = document.getElementById("places-content");
    const showIndex = document.getElementById("index");
    const showPlaces = document.getElementById("places");
    get_buttons();

    showIndex.addEventListener('click', () => {
        get_buttons();
        placesContent.classList.add('hidden');
        indexContent.classList.remove('hidden');
    });

    showPlaces.addEventListener('click', () => {
        show_places();
        indexContent.classList.add('hidden');
        placesContent.classList.remove('hidden');
    });

    function get_buttons() {
        fetch('/plotter/load_places')
        .then(response => response.json())
        .then(data => {
            data = data.data;
            const container = document.getElementById('saved-buttons');
            container.innerHTML = '';
            document.getElementById('total').innerHTML = '0';
            document.getElementById('lng-sum').innerHTML = '0';
            document.getElementById('lat-sum').innerHTML = '0';
            
            let saved_markers = [];
    
            for (let place in data) {
                const button = document.createElement('button');
                button.setAttribute('class', 'btn btn-outline-light');
                button.setAttribute('style', 'margin-right: 10px; height: 40px; width: 80px;')
                const name = data[place].name
                const lat = data[place].lat
                const lng = data[place].lng
    
                button.innerHTML = `${name}`;
    
                button.addEventListener('click', function() {
                    lat_sum = parseFloat(document.getElementById('lat-sum').innerHTML);
                    lng_sum = parseFloat(document.getElementById('lng-sum').innerHTML);
                    total = parseFloat(document.getElementById('total').innerHTML);
    
                    for (let i in saved_markers) {
                        if (saved_markers[i].title === name) {
                            lat_sum -= lat;
                            lng_sum -= lng;
                            total--;
        
                            document.getElementById('lat-sum').innerHTML = lat_sum;
                            document.getElementById('lng-sum').innerHTML = lng_sum;
                            document.getElementById('total').innerHTML = total;
    
                            saved_markers[i].setMap(null);
                            delete saved_markers[i]
    
                            return;
                        }
                    }
    
                    lat_sum += lat;
                    lng_sum += lng;
                    total++;
                    
                    let saved = new google.maps.Marker({
                        position: { lat: lat, lng: lng },
                        map: map.innerMap,
                        title: name
                    })
    
                    saved_markers.push(saved);
    
                    document.getElementById('lat-sum').innerHTML = lat_sum;
                    document.getElementById('lng-sum').innerHTML = lng_sum;
                    document.getElementById('total').innerHTML = total;
                });
    
                container.appendChild(button);
            }
        })
    }   
    // This function is used to initialize the marker for the new place-picker search bar dynamically added
    function initializePlacePicker(placePicker) {
        // First we create a separate marker for the new place-picker
        let marker = new google.maps.Marker({
            // Set its map as our map displayed on the screen
            map: map.innerMap
        });

        // Now add an EventListener to check when the new place-picker is changed
        placePicker.addEventListener('gmpx-placechange', () => {
            // Close the current infowindow
            // Get the new place and store it in a const named 'place'
            const place = placePicker.value;
            // If there's no address associated, return an error, and set marker as null
            if (!place.location) {
                window.alert("No details available for input: '" + place.name + "'");
                marker.setMap(null);  // Remove previous marker
                return;
            }

            // Otherwise, set marker at the location of the place
            marker.setPosition(place.location);
            
            // Now create an infowindow to show the address of the place above the marker 
            infowindowContent.children["place-name"].textContent = place.displayName;
            infowindowContent.children["place-address"].textContent = place.formattedAddress;
            infowindow.open(map.innerMap, marker);
            
        });

        placePicker.marker = marker;
    }

    // Create a const PlacePicker and fetch the first element with class place-picker
    const initialPlacePicker1 = document.querySelector("#place-picker-1");
    // If it exists (i.e. the user has inputted a place in the search bar), run the initializePlacePicker function
    if (initialPlacePicker1) {
        initializePlacePicker(initialPlacePicker1);
    }

    // Ensure newly created place pickers are initialized
    document.querySelector('#new-inputs').addEventListener('DOMNodeInserted', (event) => {
        if (event.target.tagName === 'GMPX-PLACE-PICKER') {
            initializePlacePicker(event.target);
        }
    }); 
}

function deleteInputFields() {
    const placePickerToDelete = document.querySelector(".place-picker");
    if (placePickerToDelete) {
        placePickerToDelete.remove(); // Remove the input element

        // Remove associated marker
        if (placePickerToDelete.marker) {
            placePickerToDelete.marker.setMap(null); // Remove marker from map
            delete placePickerToDelete.marker; // Remove reference to marker
        }
    }
}

// Function to create new input field with class as place-picker
function createNewInputFields() {
    const container = document.getElementById('new-inputs');
  
    const newElem = document.createElement("gmpx-place-picker");
    newElem.setAttribute("for-map", "map");
    newElem.classList.add("place-picker");
  
    container.insertBefore(newElem, container.firstChild);
  
    initializePlacePicker(newElem);
}


function sendData() {

    if (midpoint_marker) {
        midpoint_marker.setMap(null); // Remove marker from map
        delete midpoint_marker; // Remove reference to marker
    }
    
    const elements = Array.from(document.querySelectorAll('.place-picker'));

    var filter = document.getElementById("filter");
    filter = filter.value;

    const saved_lat = parseFloat(document.getElementById('lat-sum').innerHTML);
    const saved_lng = parseFloat(document.getElementById('lng-sum').innerHTML);
    const total = parseFloat(document.getElementById('total').innerHTML);

    if (((elements.length) + total) < 2) {
        alert('Must input atleast 2 places.');
        throw new Error('Less than 2 places inputted.');
    }

    const saved_data = {'lat': saved_lat, 'lng': saved_lng, 'total': total};

    function getCsrfToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }

    addresses = [];

    if (elements) {
        elements.every(element => {
            // Assuming .value holds the location data
            address = element.value.formattedAddress;
            addresses.push(address);
            return true;
        });
    }


    const data = {
        addresses: addresses,
        filter: filter,
        saved_data: saved_data
    }

    fetch('/plotter/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Network response was not ok');
        }
    })
    .then(data => {
        centroid = data['data']['centroid'];
        addresses = data['data']['addresses'];
        places = data['data']['places'];

   
        //const image = 'https://www.simpleimageresizer.com/_uploads/photos/ac52f17e/centroid_marker_optimized.png';
        let marker = new google.maps.Marker({
            // Set its map as our map displayed on the screen
            map: map.innerMap,
            //icon: image,
        });


        centroid = { lat: centroid[0], lng: centroid[1] };
        marker.setPosition(centroid);

        // Hide or reset infowindow content
        infowindow.close();

        display_results(places);

        midpoint_marker = marker;

    })
}

function display_results(places) {
    document.getElementById('results').innerHTML = '';
    results = document.querySelector('#results');
  
    for (let i in places) {
        content = document.createElement('li')
        content.setAttribute('class', 'content')

        place = places[i]
        place_name = place['name']

        content.setAttribute('id', i)

        place_dist = place['dist']
    
        place_vic = place['vic']
        place_types = place['types']
        place_photo = place['photo']

        content.innerHTML = `<p><b>${place_name}</b></p> <p>${place_vic}</p> <p>${place_dist} km from center</p>`;

        content.addEventListener('click', function() {
            window.open(place_photo, '_blank');
        });

        results.appendChild(content, results.firstChild);
    }

    document.querySelector('#results').style.display = 'block';

    results.addEventListener('mouseover', function() {
        const hover = event.target.closest('.content');
        if (hover && results.contains(hover)) {
            hover.style.backgroundColor = 'grey';
        }
    });

    results.addEventListener('mouseout', function() {
        const out = event.target.closest('.content');
        if (out && results.contains(out)) {
            out.style.backgroundColor = 'white';
        }
    });


}

function add_place() {
    var name = document.getElementById('new-name');
    var address = document.getElementById('new-address');
    console.log(address.value.location, address.value.formattedAddress);
    address = address.value.formattedAddress;
    name = name.value;
    console.log(name, address);

    data = {'name': name, 'address': address, 'location': location}

    function getCsrfToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }

    fetch('/plotter/add_place', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Network response was not ok');
        }
    })
    .then(data => {
        console.log(data);
        show_places();
    })

}

function show_places() {
    fetch('/plotter/load_places')
    .then(response => response.json())
    .then(data => {
        const list = document.getElementById('show-places');
        list.innerHTML = '';
        console.log(data);

        data = data.data
        for (let i in data) {
            pair = data[i]
            console.log(pair)
            item = document.createElement('div')
            item.setAttribute("class", "content")

            remove = document.createElement('button')
            remove.innerHTML = 'DELETE'
            remove.setAttribute('class', 'btn btn-outline-danger')

            name = pair['name']
            address = pair['address']

            item.innerHTML = `<h4>${name}</h4><h6>${address}</h6> `

            item.appendChild(remove);

            remove.addEventListener('click', (event) => {
                delete_place = event.target.closest('.content')
                name = delete_place.querySelector('h4').textContent;

                function getCsrfToken() {
                    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
                }

                fetch('/plotter/delete_place', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    },
                    body: JSON.stringify(name)
                })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Network response was not ok');
                    }
                })
                .then(data => {
                    console.log(data.message);
                    show_places()
                })
            })
            list.appendChild(item, list.firstChild);
        }
        })
}







document.addEventListener('DOMContentLoaded', init);

/* Breakdown of this process

Step 1: Create an initialize place picker function, and initialize it's marker and an 
add EventListener to update the marker.

Step 2: Pass the intial (1st) place picker to the function just made and initialize it.

Step 3: Create a function to pass any new place pickers dynamically created using
ad event listener to check for new DOMNodes.

I tried to send the data using the fetch POST method in the code below, but I'm getting a 404 error on my console.

*/