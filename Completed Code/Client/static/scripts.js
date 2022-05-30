let game_over = true
var board,
  game = new Chess(),
  statusEl = $('#status'),
  fenEl = $('#fen'),
  pgnEl = $('#pgn');

/* Initialize Chessboard with chess.js */
setTimeout(function () {
  board = ChessBoard('board', cfg);
}, 0);

var onDragStart = function (source, piece, position, orientation) {
  if (game.game_over() === true ||
    (game.turn() === 'w' && piece.search(/^b/) !== -1) ||
    (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
    return false;
  }
};

/* Move pieces on the chessboard when player drop the piece*/
var onDrop = function(source, target) {
  // Check if move is legal
  var move = game.move({
    from: source,
    to: target,
    promotion: 'q' //Always promote to a queen for simplicity
  });

  // If illegal move snapback the position
  if (move === null) return 'snapback';

  updateStatus();
  getResponseMove();
};

/* Update board position after piece snap from castling, en passant, pawn promotion*/
var onSnapEnd = function() {
    board.position(game.fen());
};

/* Update Status of the game to be displayed */
var updateStatus = function() {
  var status = '';

  var moveColor = 'White';
  if (game.turn() === 'b') {
    moveColor = 'Black';
  }

  if (game_over === true){
    gameover();
    game_over = false;
  }

  // Check if the game is in checkmate
  if (game.in_checkmate() === true) {
    status = 'Game over, ' + moveColor + ' is in checkmate.';
  }

  // Check if the game is in a draw
  else if (game.in_draw() === true) {
    status = 'Game over, drawn position';
  }

  // Game is still continuing
  else {
    status = moveColor + ' to move';

    // Position in check
    if (game.in_check() === true) {
      status += ', ' + moveColor + ' is in check';
    }
  }

  setStatus(status);
  createTable();
  updateScroll();

  statusEl.html(status);
  fenEl.html(game.fen());
  pgnEl.html(game.pgn());
};


/* Send to Flask api when game is over */
var gameover = function() {
  $.post($SCRIPT_ROOT + "/gameover/", function(){})
}

/* Get move from Flask api */
var getResponseMove = function() {
    var e = document.getElementById("sel1");
    var depth = e.options[e.selectedIndex].value;
    fen = game.fen()
    $.get($SCRIPT_ROOT + "/move/" + depth + "/" + fen, function(data) {
        game.move(data, {sloppy: true});
        updateStatus();
        setTimeout(function(){ board.position(game.fen()); }, 100);
    })
}

var setPGN = function() {
  var table = document.getElementById("pgn");
  var pgn = game.pgn().split(" ");
  var move = pgn[pgn.length - 1];
}

var createTable = function() {

    var pgn = game.pgn().split(" ");
    var data = [];

    for (i = 0; i < pgn.length; i += 3) {
        var index = i / 3;
        data[index] = {};
        for (j = 0; j < 3; j++) {
            var label = "";
            if (j === 0) {
                label = "moveNumber";
            } else if (j === 1) {
                label = "whiteMove";
            } else if (j === 2) {
                label = "blackMove";
            }
            if (pgn.length > i + j) {
                data[index][label] = pgn[i + j];
            } else {
                data[index][label] = "";
            }
        }
    }

    $('#pgn tr').not(':first').remove();
    var html = '';
    for (var i = 0; i < data.length; i++) {
        html += '<tr><td>' + data[i].moveNumber + '</td><td>'
        + data[i].whiteMove + '</td><td>'
        + data[i].blackMove + '</td></tr>';
    }

    $('#pgn tr').first().after(html);
}

var updateScroll = function() {
    $('#moveTable').scrollTop($('#moveTable')[0].scrollHeight);
}

var setStatus = function(status) {
  document.getElementById("status").innerHTML = status;
}

/* Configuration for the chessboard */
// configuration should be initialized after all onDragStart, OnDrop, onSnapEnd function has be initialized
var cfg = {
  draggable: true,
  position: 'start',
  onDragStart: onDragStart,
  onDrop: onDrop,
  onSnapEnd: onSnapEnd
};

/* Takeback function to allow take back */
var takeBack = function() {
    game.undo();
    if (game.turn() != "w") {
        game.undo();
    }
    board.position(game.fen());
    updateStatus();
}

/* New game function to allow a new game to be made */
var newGame = function() {
    game.reset();
    board.start();
    updateStatus();
    game_over = true;
}
