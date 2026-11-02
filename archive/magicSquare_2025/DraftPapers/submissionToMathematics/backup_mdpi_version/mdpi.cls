%%
%% mdpi.cls - Fallback MDPI document class for Mathematics journal
%% This is a simplified version that defines necessary commands
%%
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{mdpi}[2025/06/23 Fallback MDPI class]

% Process options
\DeclareOption{article}{\def\@journal{article}}
\DeclareOption{submit}{\def\@submit{true}}
\DeclareOption{moreauthors}{\def\@moreauthors{true}}
\DeclareOption{pdftex}{\def\@pdftex{true}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

% Load base class
\LoadClass[10pt,a4paper]{article}

% Required packages
\RequirePackage{geometry}
\RequirePackage{fancyhdr}
\RequirePackage{natbib}
\RequirePackage{graphicx}
\RequirePackage{times}
\RequirePackage{xcolor}
\RequirePackage{amsmath,amssymb,amsfonts}

% Page geometry
\geometry{
  left=2.5cm,
  right=2.5cm,
  top=2.5cm,
  bottom=2.5cm
}

% Define MDPI-specific commands
\newcommand{\firstpage}[1]{\gdef\@firstpage{#1}}
\newcommand{\pubvolume}[1]{\gdef\@pubvolume{#1}}
\newcommand{\issuenum}[1]{\gdef\@issuenum{#1}}
\newcommand{\articlenumber}[1]{\gdef\@articlenumber{#1}}
\newcommand{\pubyear}[1]{\gdef\@pubyear{#1}}
\newcommand{\copyrightyear}[1]{\gdef\@copyrightyear{#1}}
\newcommand{\externaleditor}[1]{\gdef\@externaleditor{#1}}
\newcommand{\datereceived}[1]{\gdef\@datereceived{#1}}
\newcommand{\dateaccepted}[1]{\gdef\@dateaccepted{#1}}
\newcommand{\datepublished}[1]{\gdef\@datepublished{#1}}
\newcommand{\hreflink}[1]{\gdef\@hreflink{#1}}

% Title and author commands
\newcommand{\Title}[1]{\title{#1}}
\newcommand{\Author}[1]{\author{#1}}
\newcommand{\AuthorNames}[1]{\gdef\@authornames{#1}}
\newcommand{\address}[1]{\gdef\@address{#1}}
\newcommand{\corres}[1]{\gdef\@corres{#1}}

% Abstract and keywords
\renewcommand{\abstract}[1]{\gdef\@abstract{#1}}
\newcommand{\keyword}[1]{\gdef\@keyword{#1}}

% External bibliography
\newcommand{\externalbibliography}[1]{\gdef\@externalbib{#1}}

% Header and footer setup
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\footnotesize Mathematics \@pubyear{}, \@pubvolume{}, \@articlenumber}
\fancyhead[R]{\footnotesize \thepage}
\renewcommand{\headrulewidth}{0.4pt}
\fancyfoot[C]{\footnotesize \textcopyright{} \@copyrightyear{} by the authors.}

% Redefine maketitle
\renewcommand{\maketitle}{%
  \thispagestyle{empty}
  \begin{center}
    {\Large\bfseries\@title\par}
    \vspace{1em}
    {\@author\par}
    \vspace{0.5em}
    {\small\@address\par}
    \vspace{0.5em}
    {\small\@corres\par}
  \end{center}
  \vspace{1em}
  \noindent\textbf{Abstract:} \@abstract
  \vspace{0.5em}
  
  \noindent\textbf{Keywords:} \@keyword
  \vspace{1em}
}

% Section formatting
\renewcommand\section{\@startsection{section}{1}{\z@}%
  {-3.5ex \@plus -1ex \@minus -.2ex}%
  {2.3ex \@plus.2ex}%
  {\normalfont\large\bfseries}}

\renewcommand\subsection{\@startsection{subsection}{2}{\z@}%
  {-3.25ex\@plus -1ex \@minus -.2ex}%
  {1.5ex \@plus .2ex}%
  {\normalfont\normalsize\bfseries}}

% Initialize variables
\firstpage{1}
\pubvolume{xx}
\issuenum{1}
\articlenumber{0}
\pubyear{2025}
\copyrightyear{2025}
\externaleditor{Academic Editor: Name}
\datereceived{}
\dateaccepted{}
\datepublished{}
\hreflink{}

\endinput