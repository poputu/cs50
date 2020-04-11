#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    //Insure used argument
    if (argc == 1)
    {
        printf("Usage: ./ recover.c file to recover\n");
        return 1;
    }
    //insure user give one argument
    if (argc > 2)
    {
        printf ("Use only one argument (file to recover)\n");
        return 1;
    }
    
    // Name for our file, and we use 2 because we use only one argv
    char *infile = argv[1];
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 4;
    }
    unsigned char *buffer = malloc(512);// make space for data from flash
    int counter = 0; 
    FILE *image;
    char image_name[8];
    // we read to buffer from file inptr with size of 512
    while( fread(buffer, 512, 1, inptr))
    {
        //rules for jpeg header
        //(buffer[3] & 0xf0) == 0xe0 use this to ignore 0 in 0xf0, you can move 0 so first on other bit will be ignored
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //check if this first time
            if (counter > 0)
            {
                fclose(image);
            }
            // create image_name
            sprintf(image_name, "%03d.jpg", counter);
            // open new image file
            image = fopen(image_name, "w");
            if (image == NULL)
            {
                printf(" cannot write a image %s", image_name);
                fclose(image);
                free(buffer);
                return 5;
            }
            counter++;

        }
        //check if we have found jpeg and write it, code above will start only if we found new one
        //if not we will continue to write old file
        if( counter > 0)
        {
            fwrite(buffer, 512, 1, image);
        }
        
    }
    free(buffer);
    fclose(image);
    fclose(inptr);
    
}
