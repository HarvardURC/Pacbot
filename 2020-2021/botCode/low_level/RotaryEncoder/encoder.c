#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <pigpio.h>

typedef void (*Pi_Renc_CB_t)(int, int);

struct _Pi_Renc_s;

typedef struct _Pi_Renc_s Pi_Renc_t;

Pi_Renc_t * Pi_Renc(int gpioA, int gpioB, Pi_Renc_CB_t callback, int enc);

void Pi_Renc_cancel(Pi_Renc_t *renc);

struct _Pi_Renc_s
{
   int gpioA;
   int gpioB;
   Pi_Renc_CB_t callback;
   int levA;
   int levB;
   int lastGpio;
   int enc;
};

static void _cb(int gpio, int level, uint32_t tick, void *user)
{
  Pi_Renc_t *renc;

  renc = user;

  if (gpio == renc->gpioA) renc->levA = level; else renc->levB = level;

  if (gpio != renc->lastGpio) /* debounce */
  {
    renc->lastGpio = gpio;

    if ((gpio == renc->gpioA) && (level == 1))
    {
      if (renc->levB) {
        (renc->callback)(1, renc->enc);
      } else {
        (renc->callback)(-1, renc->enc);
      }

    }
    else if ((gpio == renc->gpioB) && (level == 1))
    {
      if (renc->levA) {
        (renc->callback)(-1, renc->enc);
      } else {
        (renc->callback)(1, renc->enc);
      }
    }
  }
};

Pi_Renc_t * Pi_Renc(int gpioA, int gpioB, Pi_Renc_CB_t callback, int enc)
{
   Pi_Renc_t *renc;

   renc = malloc(sizeof(Pi_Renc_t));

   renc->gpioA = gpioA;
   renc->gpioB = gpioB;
   renc->callback = callback;
   renc->levA=0;
   renc->levB=0;
   renc->lastGpio = -1;
   renc->enc=enc;

   gpioSetMode(gpioA, PI_INPUT);
   gpioSetMode(gpioB, PI_INPUT);

   /* pull up is needed as encoder common is grounded */

   gpioSetPullUpDown(gpioA, PI_PUD_UP);
   gpioSetPullUpDown(gpioB, PI_PUD_UP);

   /* monitor encoder level changes */

   gpioSetAlertFuncEx(gpioA, _cb, renc);
   gpioSetAlertFuncEx(gpioB, _cb, renc);

   return renc;
};
void Pi_Renc_cancel(Pi_Renc_t *renc)
{
    if (renc)
    {
       gpioSetAlertFunc(renc->gpioA, 0);
       gpioSetAlertFunc(renc->gpioB, 0);

       free(renc);
    }
 };

/*

REQUIRES

A rotary encoder contacts A and B connected to separate gpios and
the common contact connected to Pi ground.

TO BUILD

gcc -o rot_enc_c test_rotary_encoder.c rotary_encoder.c -lpigpio -lrt

TO RUN

sudo ./rot_enc_c

*/

static int posA = 0;
Pi_Renc_t * rencA;

static int posB = 0;
Pi_Renc_t * rencB;


void encoderCallback(int way, int enc)
{
  if (enc == 0) {
    posA += way;
  } else {
    posB += way;
  }
};

static PyObject* encoderRead(PyObject* self, PyObject* args){
  int n;
  if(!PyArg_ParseTuple(args, "i", &n))
    return NULL;
  if (n == 0) {
    return Py_BuildValue("i", posA);
  } else {
    return Py_BuildValue("i", posB);
  }
};

static PyObject* encoderWrite(PyObject* self, PyObject* args){
  int n;
  int enc;
  // if our `n` value 
  if(!PyArg_ParseTuple(args, "ii", &n, &enc))
    return NULL;
  
  if (enc == 0) {
    posA = n;
  } else {
    posB = n;
  }
  return Py_None;
};

static PyObject* encoderInit(PyObject* self, PyObject* args)
{	
  int pin_a, pin_b, enc;

  if(!PyArg_ParseTuple(args, "iii", &pin_a, &pin_b, &enc))
    return NULL;
   
  if (gpioInitialise() < 0) return Py_BuildValue("i", 1);

  if (enc == 0) {
    rencA = Pi_Renc(pin_a, pin_b, encoderCallback, enc);
  } else {
    rencB = Pi_Renc(pin_a, pin_b, encoderCallback, enc);
  }

  return Py_None;

};

static PyObject* encoderTerminate(PyObject* self, PyObject* args){
  Pi_Renc_cancel(rencA);
  Pi_Renc_cancel(rencB);

  gpioTerminate();

  return Py_None;
};

static PyMethodDef encoderMethods[] = {
  {"init", encoderInit, METH_VARARGS, "Initialize Encoder"},
  {"terminiate", encoderTerminate, METH_NOARGS, "Terminate Encoder"},
  { "write", encoderWrite, METH_VARARGS, "Write Encoder Value" },
  { "read", encoderRead, METH_VARARGS, "Read Encoder" },
  { NULL, NULL, 0, NULL }
};

// Our Module Definition struct
static struct PyModuleDef Encoder = {
  PyModuleDef_HEAD_INIT,
  "Encoder",
  "Encoder Module",
  -1,
  encoderMethods
};

// Initializes our module using our above struct
PyMODINIT_FUNC PyInit_Encoder(void)
{
  return PyModule_Create(&Encoder);
}
