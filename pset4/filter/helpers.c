#include "helpers.h"
#include <string.h>
#include <stdio.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //printf ("%d\n",copy_image[i][j].rgbtBlue);
            BYTE d = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.00);
            image[i][j].rgbtBlue = d;
            image[i][j].rgbtGreen = d;
            image[i][j].rgbtRed = d;

        }
    }
    //image = &copy_image;
    return;
}

// Reflect image horizontally
/*void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[1][1];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j <= (round(width / 2.00)); j++)
        {
            temp[0][0] = image[i][j];
            image[i][j] = image[i][width-j-1];
            image[i][width-j-1] = temp[0][0];

        }
    }
    return;
    // цей варіант не працює, висновок: не можна стуктури копіювати, треба копіювати байти
}*/

void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //use of a temporary array to swap values
    int temp[3];
    for (int j = 0; j < height; j++)
    {
        for (int i = 0; i < width / 2; i++)
        {
            temp[0] = image[j][i].rgbtBlue;
            temp[1] = image[j][i].rgbtGreen;
            temp[2] = image[j][i].rgbtRed;

            // swap pixels with the ones on the opposite side of the picture and viceversa
            image[j][i].rgbtBlue = image[j][width - i - 1].rgbtBlue;
            image[j][i].rgbtGreen = image[j][width - i - 1].rgbtGreen;
            image[j][i].rgbtRed = image[j][width - i - 1].rgbtRed;

            image[j][width - i - 1].rgbtBlue = temp[0];
            image[j][width - i - 1].rgbtGreen = temp[1];
            image[j][width - i - 1].rgbtRed = temp[2];
        }
    }
}


// Blur image

// I was make by myself but my version do not make it blur like check50 likes, but blur it
//https://github.com/Federico-abss/CS50-intro-course/blob/master/C/pset4/filter/helpers.c
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int tempBlue;
    int tempGreen;
    int tempRed;
    float divider;
    RGBTRIPLE temp[height][width];

    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            tempBlue = 0;
            tempGreen = 0;
            tempRed = 0;
            divider = 0.00;


            // sums values of the pixel and 8 neighboring ones, skips iteration if it goes outside the pic
            for (int k = -1; k < 2; k++)
            {
                if (j + k < 0 || j + k > height - 1)
                {
                    continue;
                }

                for (int h = -1; h < 2; h++)
                {
                    if (i + h < 0 || i + h > width - 1)
                    {
                        continue;
                    }

                    tempBlue += image[j + k][i + h].rgbtBlue;
                    tempGreen += image[j + k][i + h].rgbtGreen;
                    tempRed += image[j + k][i + h].rgbtRed;
                    divider++;
                }
            }
            if (divider == 0)
            {
                printf("we divided by 0");
            }
            temp[j][i].rgbtBlue = round(tempBlue / divider);
            temp[j][i].rgbtGreen = round(tempGreen / divider);
            temp[j][i].rgbtRed = round(tempRed / divider);


        }

    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    long sum_red_x, sum_blue_x, sum_green_x;
    long sum_red_y, sum_blue_y, sum_green_y;
    RGBTRIPLE temp[height][width];
    RGBTRIPLE temp_x[4][4];
    RGBTRIPLE temp_y[4][4];
    // I use Gx Gy like array for formula 
    // this arrays help to loop our calculate
    int arx[4][4] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int ary[4][4] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};



    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            sum_red_x = 0, sum_blue_x = 0, sum_green_x = 0;
            sum_red_y = 0, sum_blue_y = 0, sum_green_y = 0;

            for (int i2 = 0; i2 < 3; i2++)
            {
                for (int j2 = 0; j2 < 3; j2++)
                {
                    // this check if we out of board and draw black pixel if we are out of board
                    if ((i + i2 - 1) < 0 || (i + i2 - 1) > (height - 1) || (j + j2 - 1) < 0 || (j + j2 - 1) > (width - 1))
                    {
                        temp_x[i2][j2].rgbtBlue = 0;
                        temp_x[i2][j2].rgbtGreen = 0;
                        temp_x[i2][j2].rgbtRed = 0;
                    }
                    else
                    {
                        temp_x[i2][j2].rgbtBlue = image[i + i2 - 1][j + j2 - 1].rgbtBlue;
                        temp_x[i2][j2].rgbtGreen = image[i + i2 - 1][j + j2 - 1].rgbtGreen;
                        temp_x[i2][j2].rgbtRed = image[i + i2 - 1][j + j2 - 1].rgbtRed;

                    }
                    // this make what task call Gx
                    // arx change so we calculate here with The Sobel filter in one line!
                    sum_blue_x += temp_x[i2][j2].rgbtBlue * arx[i2][j2];
                    sum_green_x += temp_x[i2][j2].rgbtGreen * arx[i2][j2];
                    sum_red_x += temp_x[i2][j2].rgbtRed * arx[i2][j2];
                    sum_blue_y += temp_x[i2][j2].rgbtBlue * ary[i2][j2];
                    sum_green_y += temp_x[i2][j2].rgbtGreen * ary[i2][j2];
                    sum_red_y += temp_x[i2][j2].rgbtRed * ary[i2][j2];
                }
            }
            // make the new value for pixel
            // use long because int can out reach
            long final_blue = 0, final_red = 0, final_green = 0;
            final_blue = round(sqrt((pow(sum_blue_x, 2)) + (pow(sum_blue_y, 2))));
            final_red = round(sqrt((pow(sum_red_x, 2)) + (pow(sum_red_y, 2))));
            final_green = round(sqrt((pow(sum_green_x, 2)) + (pow(sum_green_y, 2))));
            //make if for max 255
            if (final_blue > 255)
            {
                final_blue = 255;
            }
            if (final_red > 255)
            {
                final_red = 255;
            }
            if (final_green > 255)
            {
                final_green = 255;
            }
            // make shure you use int, not long
            temp[i][j].rgbtBlue = (int)final_blue;
            temp[i][j].rgbtGreen = (int)final_green;
            temp[i][j].rgbtRed = (int)final_red;

        }
    }
    //this loop make final image from temp
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
        }
    }


    return;
}
