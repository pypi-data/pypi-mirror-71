//
// Created by 谢建 on 2020-06-03.
//

#ifndef PYSAMPLE_SAMPLE_COUNTER_H
#define PYSAMPLE_SAMPLE_COUNTER_H

#include "Python.h"

#include "hash_map.h"
#include "frameobject.h"
#include "sample_traceback.h"


typedef struct {
    int count;
    SampleTraceback *traceback;
} SamplePoint;


typedef struct {
    int delta;
    PyObject *sys_path;
    HashMap *filenames;         // filename deduplication
    HashMap *short_filenames;   // short filenames cache
    HashMap *points;            // map SampleTraceback to SamplePoint
} SampleCounter;


SampleCounter *SampleCounter_Create(int delta, PyObject *sys_path);

void SampleCounter_Free(SampleCounter *counter);

int SampleCounter_AddFrame(SampleCounter *counter, PyObject *frame);

int SampleCounter_AddTraceback(SampleCounter *counter, SampleTraceback *traceback);

PyObject *SampleCounter_FlameOutput(SampleCounter *counter);


#endif //PYSAMPLE_SAMPLE_COUNTER_H
