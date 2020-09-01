window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

function deleteRecord(model, id) {
  fetch(`/${model}/${id}`, {
    method: 'DELETE'
  }).then(res => res.json())
    .then(res => {
      // alert(res.message)
      // window.location.href = '/'
    })
}

function deleteVenue(venueId) {
  deleteRecord('venues', venueId)
  $('#modal-title').text(`Delete Venue ${venueId}`)
  $('#modal-message').text(`Venue with id ${venueId} deleted successfully!`)
  $('#delete-venue-modal').modal('show');
}

function deleteArtist(artistId) {
  deleteRecord('artists', artistId);
  $('#modal-title').text(`Delete Artist ${artistId}`)
  $('#modal-message').text(`Artist with id ${artistId} deleted successfully!`)
  $('#delete-artist-modal').modal('show');
}

function deleteShow(showId) {
  deleteRecord('shows', showId);
  $('#modal-title').text(`Delete Show ${showId}`)
  $('#modal-message').text(`Show with id ${showId} deleted successfully!`)
  $('#delete-show-modal').modal('show');
}

function redirectTo(url) {
  window.location.href = url;
}
