/**** Variable Declarations ****/

const DEFAULT_BALL_Y = 430;
const INITIAL_VELOCITY = 1;
const INITIAL_SCORE = 0;
const MARGIN = 10;

let posX; 
let posY;
let dirX; 
let dirY; 
let score;
let speed;
let stripes;
let newGameActive = false;
let ball_width_val = BALL_WIDTH;
let ball_height_val = BALL_HEIGHT;

// These variables must be synchronized with the ones created in pdf_generator.py
let instruction = this.getField('instruction');
let newGameButton = this.getField('newGameButton');
let ball = this.getField('ball');
let bar = this.getField('bar');
let scoreArea = this.getField('scoreArea');
let start_screen = this.getField('start_screen'); // NEW: start screen overlay
let renderer = this.getField('renderer');


/**** Functions ****/

function initialize() {
    if (global.initialized) return; // Prevent multiple initializations    
    if (newGameActive) {        
        global.initialized = true;
        setupGame();        
        startGame();
    } else {        
        resetGameView(); // Hide all game fields until 'New Game' is pressed
    }
}

// Initialize game parameters
function setupGame() {
    posX = randomBallX();
    posY = DEFAULT_BALL_Y;
    dirX = 2;
    dirY = 2;
    stripes = []; // Mouse tracker
    speed = INITIAL_VELOCITY; // Ball speed
    score = INITIAL_SCORE;  
    global.mouseX = posX + ball_width_val / 2;
    hideStripes();    
}

function randomBallX(){
    return (Math.floor(Math.random() * (CANVAS_WIDTH - ball_width_val - MARGIN * 2)) + MARGIN);
}

function hideStripes(){
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
        update();
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
}

function update(){
    checkCollision();
    moveBall(speed);
}

function checkCollision() {    
    if (posX + dirX > CANVAS_WIDTH - ball_width_val || posX + dirX < 0) {
        dirX = -dirX;    
    }

    if (posY + dirY > CANVAS_BASE + CANVAS_HEIGHT - ball_height_val) {
        dirY = -dirY;    

    } else if (posY + dirY < BAR_BASE_DISTANCE + BAR_HEIGHT) {
        if (posX + ball_width_val > barPosX() && posX < barPosX() + BAR_WIDTH) {
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
    ball_height_val = ball_height_val / divisorHeight;
    ball_width_val = ball_width_val / divisorWidth;
}

function endGame() {
    global.initialized = false;
    app.clearInterval(gameLoop); // Stop game loop
    ball_width_val = BALL_WIDTH; // Reset ball width
    ball_height_val = BALL_HEIGHT; // Reset ball height
    score = 0; // Reset score
    initialize();
}

function resetGameView() {
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
        posX, posY, posX + ball_width_val, posY + ball_height_val
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
