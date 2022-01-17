# GTM data grabber

## **Summary** 
### **Problem** 
I'm working on a documentation project for a client 
The client has been upgraded from Universal Analytics (UA) to Google Analytics 4 (GA4), so the documentation needs information like which Google Tag Manager (GTM) tags have been kept, combined, deleted and what is the naming events naming convention is on GA4.

Since I did not work on  the GA4 implementation I did not know what events where kept, combined, or deleted, so I needed to go over all the tags in GTM to figure understand the implementation first. That alone is a cumbersome task since there are 110+ tags for UA alone.

### **Solution** 
GTM offers the option to export all tags in a GTM container and workspace. The export is a JSON file, that uses the same notation as the [GTM API](https://developers.google.com/tag-platform/tag-manager/api/v2). So I exported the GTM Container I need to analyze and got to coding a script that will export all the UA tags, including the tracking type, event Category/Action/Label, custom dimensions (cd), custom metrics (cm), triggers, and blocking triggers, and all ga4 tags, including event names and event parameters. 

## **GTM JSON export** 
*P.S: given that gtm.json file I used contains client sensitive information, I added the file to .gitignore.*

***To try out this code you do need to export a GTM container on your own***

The JSON export seems a bit complex at first glance, but once you start dissecting it the file becomes super easy to understand. 

The top level key value pairs are
1. exportFormatVersion – refers to the API version which is currently version 2 
2. exportTime – refers to the date and time of the export
3. containerVersion – contains all the fun stuff that we need to get into! the value for this key is a json object

containerVersion has 13 key value pairs which I will explain in detail

1. path
2. accountId
3. containerId
4. containerVersionId
5. container
6. tag
7. trigger
8. variable
9. folder
10. builtInVariable
11. fingerprint
12. tagManagerUrl
13. customTemplate

### path, accountId, containerId, containerVersionId 
This key value contains the API endpoint used to get the information