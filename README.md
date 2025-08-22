# Emoji Flowchart Builder

An online tool where you use emojies to make a flowchart.

## 🌀 The Story of Emoji Flowchart Builder

It all started at a Python Code Jam, where the theme was: “Wrong Tool for the Job.”
Our team looked at each other and thought:

> “What could be more wrong than using Python to run in the browser… inside WebAssembly?”

Minhaz, our fearless leader, said:

> “Let’s do it. Let’s bend Python until it speaks the language of the web.”

Saad grinned:

> “And while we’re at it, let’s reinvent flowcharts… but with emojis!”

NaviTheCoderboi laughed:

> “Yes! Because who needs rectangles and diamonds when you can have 😃🔥🚀💡?”

Apoorv, the architect, reminded us:

> “It should still work though… even if it looks like fun.”

And Rabbiya, the creative spark, added:

> “Exactly. Flowcharts shouldn’t feel like homework, they should feel like play.”

So, with the “wrong tool” in hand, we built something unexpectedly right:

> ✨ Emoji Flowchart Builder ✨

A Python-powered, browser-ready app where ideas flow not through dull boxes, but through the universal language of emojis.

And that’s how our team — Minhaz, Saad, NaviTheCoderboi, Apoorv, and Rabbiya — turned the wrong tool for the job into the perfect tool for creativity.

## How to run

### Run with docker

We have a very simple docker setup for the project. You can run the project with docker.

Make sure you have docker installed in your computer.

### 0. Clone the repo

> Note: this assumes you have git installed

Navigate to the desired location and clone this repository

```shell
git clone https://github.com/minhaz1217/fearless-ferns
```

Then, navigate to the newly created folder

```shell
cd fearless-ferns
```

### 1. Build the image

To build the just run this command from the root of the project

```shell
docker build -t fearless_ferns_image .
```

### 2. Run the docker image

Run the docker image using this command

```shell
docker run -dit --name fearless_ferns -p8081:8081 fearless_ferns_image
```
If done correctly, the project will be locally hosted on port `:8081` so you can access using [localhost:8081](http://localhost:8081)
We will discuss its functionality next.


### Run by building from source

If you don't have a docker installed, do the following:

### 0. Clone the repo

> Note: this assumes you have git installed

Navigate to the desired location and clone this repository

```shell
git clone https://github.com/minhaz1217/fearless-ferns
```

Then, navigate to the newly created folder

```shell
cd fearless-ferns
```

### 1. Activate python virtual environment

```shell
# Linux, Bash
$ source .venv/bin/activate
# Linux, Fish
$ source .venv/bin/activate.fish
# Linux, Csh
$ source .venv/bin/activate.csh
# Linux, PowerShell Core
$ .venv/bin/Activate.ps1
# Windows, cmd.exe
> .venv\Scripts\activate.bat
# Windows, PowerShell
> .venv\Scripts\Activate.ps1
```

### 2. Install the dependencies

It is recommended to update your `pip` (and other stuff) first

```shell
pip install -U pip setuptools wheel
```

Then proceed to install all the dependencies

```shell
pip install -r requirements.txt
```

### 3. Install as a package

We structured our project in a way that makes it works as a package. This step is necessary, sorry.

```shell
pip install -e .
```

### 4. Running the project

Here you go

```shell
python src/project/main.py
```

If done correctly, this will open up a new tab in your default browser.
The project will be locally hosted on port `:8081`.
We will discuss its functionality next.

## How to use

### Accessing the app

Upon running this project, it will be hosted at [http:127.0.0.1:8081](http:127.0.0.1:8081).

### Description of the UI

You will see a header with the name of our team and two links, one of them, the editor, is opened already, the other will open a how to use page for detailed instructions.
The page itself is split in two parts.
On the right side you will see a mermaid-powered flowchart, and on the left side you will see an editor.
The editor itself has a toolbar above with many buttons arranged in groups and a toggleable emoji keyboard below.
The emoji keyboard has limited amount of emojies arranged in multiple sections or tabs.
Pressing an emoji button will insert that emoji at the cursor position in the editor.
Alternatively, you can use any emoji you want and place it in the editor even if we didn't include it in the emoji keyboard.
When you type anything in the editor, the flowchart will update automatically.
It will draw a new flowchart if your code is valid, and might show you a specific error as a notification.

### About the rules

While you are running the project locally, navigate to the `/how-to-use` page using the link in the header and have a look at the rules.
Here are some facts:

#### **Each unique emoji identifies a unique cell in the flowchart**

You might have noticed that already looking at the example already written in the editor when you open the page for the first time.

### Functionality

#### **The page is split using a splitter**

By default each compartment (the editor and the flowchart) take half the width of the screen.
You can resize each compartment using the splitter line in the middle.
Go ahead and try that!

#### **Use the toolbar to apply some formatting to your emoji-containing code**

Try making a statement **bold**, another in _italic_.
Try aligning text to center or to the right.
Try messing up the size of some text.
Try copying and pasting.
Then select all and clear formatting.
Your code still works the same.

Even better, try entering fullscreen mode so you can focus while typing in your emojies!
Try printing your code.

#### **Downloading your flowchart**

Who needs a download button when you can just take a screenshot!
If you have made any funny flowchart that you want to share with your friends,
just take a screenshot of it (or part of it) using your system utility.

#### **Saving your code**

As you are typing in something overly specific, your code is saved automatically in your tab, no cookies required.
Refresh your page and your changes will always still be there.
If you open the page in a new tab, your changes will be reset.
So by default, the life span of your code is the life span of your browser tab.
But how do we make the code live for longer?

If you look closely, there is a save button in your toolbar.
Hover over it and it displays a "Save your work" tooltip.
Click that and it will show "Your content was saved" notification.
Why this tastes like a poem?
Open a new tab, new default is set.
Your code from earlier is here to sit.

> Note: This feature only applies for new tabs.
Any code you have in any other tab will not be overriden.

## About the project

This project was built by `Fearless Ferns` team as part of the Python Discord Code Jam 2025. These are the team members and their main contributions:

|Name|Main contributions|
|--|--|
| Saad | Emoji keyboard, The text editor |
| Minhaz | The final emoji interpreter |
| NaviTheCoderboi | UI styles |
| Rabbiya | The interpreter |
| Apoorv |  |
