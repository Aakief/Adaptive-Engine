
<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">Adaptive learning system README</h3>

  <p align="center">
    The README for the project code of an Adaptive system
    <br />
    <a href="https://github.com/Aakief/Adaptive-Engine"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Aakief/Adaptive-Engine/issues">Report Bug</a>
    ·
    <a href="https://github.com/Aakief/Adaptive-Engine/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This project contains an adaptive learning system that estimates the learner abilities of a student for subjects in a test(s) using Item Response Theory (IRT). The adaptive system uses a ontology as its knowledge domain.

There are 3 Python programs in this project.
* **AdaptiveSystem.py** - The "main" program which continually takes vector input about student results and returns a CSV file containing triples of the students learner abilities.

* **Ontology.py** - Controls all operations performed on the ontology and learner dictionary

* **GenerateResults.py** - Simulates dummy results that can be used as input into the adaptive System

The aim of the project is to identify any weaknesses in a learners knowledge with the intention of the student addressing these weaknesses. This adaptive system is 1 part of a 3 component system. The other 2 are an Automatic Question Generator and a Natural Language Generation Algorithm.  

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python][Python.py]][Python-url]
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To begin, follow these simple steps to configure the required modules and code, allowing you to run the project on your local machine

### Prerequisites

Before running the code, make sure to install two Python modules using these commands:
* pip
  ```sh
  pip3 install owlready2
  pip3 install pyirt
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Aakief/Adaptive-Engine.git
   ```
2. Install pip packages
   ```sh
   pip3 install owlready2
   pip3 install pyirt
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

1. To simply run the Adaptive System ensure that Ontology.py and the food_galmat_1.9.owl file is in the same file as AdaptiveSystem.py.

   ```sh
   python3 AdaptiveSystem.py

   # Use the example input files. For the first iteration use "Eginput1.txt". For the second iteration use "Eginput2.txt".  
   ```
2. To generate your own sample input. Run GenerateResults.py, specifying the difficulty questions array. When trying to use multiple sample inputs from generate results, open a terminal and keep the adaptive system running, whilst generating new input in another terminal.

   ```sh
   # Terminal 1
   python3 GenerateResults.py

   # Terminal 2
   python3 AdaptiveSystem.py 
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Aakief Hassiem - HSSMUH018@myuct.ac.za - aakief.hassiem@gmail.com

Project Link: [https://github.com/Aakief/Adaptive-Engine](https://github.com/Aakief/Adaptive-Engine)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

I want to acknowledge the resources that were helpful during this project.

* [Owlready2](https://owlready2.readthedocs.io/en/v0.42/)
* [Pyirt](https://pypi.org/project/pyirt/)
* [GitHub Pages](https://pages.github.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/Aakief/Adaptive-Engine/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/Aakief/Adaptive-Engine/forks

[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/Aakief/Adaptive-Engine/stargazers

[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/Aakief/Adaptive-Engine/issues

[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/aakief-hassiem-604731209/

[Python.py]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
