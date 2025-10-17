/**** Variable Declarations ****/

var posX;
var posY;

var dirX;
var dirY;

var stripes;
var score;
var margin = 10; // Prevents the ball from starting inside the wall
var ball_width = BALL_WIDTH;
var ball_height = BALL_HEIGHT;
var newGameActive = false;

// These variables must be synchronized with the ones created in pdf_generator.py
var ball = this.getField('ball');
var bar = this.getField('bar');
var instruction = this.getField('instruction');
var scoreArea = this.getField('scoreArea');
var newGameButton = this.getField('newGameButton');
var start_screen = this.getField('start_screen'); // NEW: start screen overlay
var renderer = this.getField('renderer');
// app.alert(button ? "Field exists" : "Field does NOT exist");


/**** Functions ****/

function initialize() {
    if (global.initialized) return; // Prevent multiple initializations
    if (newGameActive) {
        global.initialized = true;
        setupGame();
        startGame();
    } else {
        deactivateAll(); // Hide all game fields until 'New Game' is pressed
    }
}

// Initialize game parameters
function setupGame() {
    posX = Math.floor(Math.random() * (CANVAS_WIDTH - ball_width - margin * 2)) + margin;
    posY = 430;
    dirX = 2;
    dirY = 2;

    stripes = []; // Mouse tracker
    speed = 1; // Ball speed
    score = 0;  
    global.mouseX = posX + ball_width / 2;
  
    // Hide all stripes until the game starts
    for (var fx = 0; fx < CANVAS_WIDTH; fx++) {
        stripes[fx] = this.getField('stripe' + fx);
        stripes[fx].display = display.hidden;    
    }
}

function startGame() {
    // Show all stripes to capture mouse position
    // for (var fx = 0; fx < CANVAS_WIDTH; fx++) {
    //     stripes[fx].display = display.visible;
    // }
    gameLoop = app.setInterval('renderGame()', 15); // Responsible for the infinite game loop
}

// Helper function to render PDF components in real-time
function renderGame() {  
    try {
        if (typeof global.initialized === "undefined") {
            global.initialized = true; // Game initialized flag
        }
        renderer.display = display.visible;
        draw();    
        renderer.display = display.hidden;
    } catch (e) {
        app.alert(e.toString());
    }
}

// Main game function that dynamically draws all components on screen
function draw() {  
    drawBall();
    drawBar();  
    drawScore();
    checkCollision();
    moveBall(speed);
}

function checkCollision() {    
    if (posX + dirX > CANVAS_WIDTH - ball_width || posX + dirX < 0) {
        dirX = -dirX;    
    }

    if (posY + dirY > CANVAS_BASE + CANVAS_HEIGHT - ball_height) {
        dirY = -dirY;    

    } else if (posY + dirY < BAR_BASE_DISTANCE + BAR_HEIGHT) {
        if (posX + ball_width > barPosX() && posX < barPosX() + BAR_WIDTH) {
            dirY = -dirY; // Reverse ball direction
            speed = changeBallSpeed(1.2); // Increase speed with each bar hit
            changeBallSize(1.2, 1.2); // Shrink ball slightly each hit
            score++;
            if (score == 10) {
                app.alert("Congratulations! You made 10 points. You won!");
                endGame();
            }
        } else {
            app.alert("Game Over!");
            endGame();      
        }
    }
}

function changeBallSpeed(multiplier) {
    return multiplier * speed;
}

function changeBallSize(divisorHeight, divisorWidth) {  
    ball_height = ball_height / divisorHeight;
    ball_width = ball_width / divisorWidth;
}

function endGame() {
    global.initialized = false;
    app.clearInterval(gameLoop); // Stop game loop
    ball_width = BALL_WIDTH; // Reset ball width
    ball_height = BALL_HEIGHT; // Reset ball height
    score = 0; // Reset score
    initialize();
}

function deactivateAll() {
    var fields = ['ball','bar','scoreArea','renderer'];

    for (var i = 0; i < fields.length; i++) {
        var field = this.getField(fields[i]);
        if (field) {
            field.display = display.hidden;
        }
    }

    stripes = [];
    for (var fx = 0; fx < CANVAS_WIDTH; fx++) {
        stripes[fx] = this.getField('stripe' + fx);
        stripes[fx].display = display.hidden;    
    }    
}

function moveBall(speedValue) {
    posX += dirX * speedValue;
    posY += dirY * speedValue;
}

function drawBall() {
    ball.rect = [
        posX, posY, posX + ball_width, posY + ball_height
    ];
}

// Draw the bar that tracks mouse position
function drawBar() {
    bar.rect = [
        barPosX(),
        bar.rect[1],
        barPosX() + BAR_WIDTH,
        bar.rect[3]
    ];  
}

function drawScore() {
    scoreArea.value = "Score: " + score + " / 10";
}

function drawButton() {
    button.rect = [
        0, PAGE_HEIGHT - 250, CANVAS_WIDTH, PAGE_HEIGHT - 200
    ];  
}

// Returns mouse position
function barPosX() {
    return global.mouseX - BAR_WIDTH / 2;
}

// Function called when the user clicks the "New Game" button
function onNewGameClick() {    
    start_screen.display = display.hidden;
    newGameButton.display = display.hidden;
    instruction.display = display.hidden;
    ball.display = display.visible;
    bar.display = display.visible;
    scoreArea.display = display.visible;
    newGameActive = true;
    initialize();
}


/**** Main Code ****/
app.alert("Version 1.0 - Tested and functional in Chrome or Opera!");
initialize();
