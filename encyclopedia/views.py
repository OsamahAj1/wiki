from turtle import title
from django.http import HttpResponseRedirect
from django.shortcuts import render
import markdown2
from django import forms
from random import choice

from . import util

class newpage(forms.Form):
    title = forms.CharField(label="Page Title", required="True")
    text = forms.CharField(widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    """show entry to user"""

    # check if it's empty
    if not util.get_entry(title):

        # return error if it's empty
        return render(request, "encyclopedia/error.html", {
            "error": "ERROR: Requested Page Was Not Found!"
        })
    
    # get the page and converte it to html and render it
    page = util.get_entry(title)
    html = markdown2.markdown(page)
    return render(request, "encyclopedia/entry.html", {
        "html": html,
        "title": title
    })

def search(request):
    """search entry"""

    # get what user typed
    q = request.GET.get("q")

    # get entry list
    entries = util.list_entries()

    # if entry in website redirect user to it
    for entry in entries:
        if entry.lower() == q.lower():
            return HttpResponseRedirect(f"/wiki/{entry}")

    # else show page with sub string of user search
    return render(request, "encyclopedia/search.html", {
        "entries": entries,
        "q": q
    })

def create(request):
    """create new page if post and show the create page if get"""

    # if post create new page
    if request.method == "POST":
        
        # get the form from user
        form = newpage(request.POST)

        # check if form valid
        if form.is_valid():

            # get form data
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]

            # check if page not already in system
            if util.get_entry(title) is not None:
                return render(request, "encyclopedia/error.html", {
                    "error": "ERROR: Page Already Existed"
                })
        
        # save page to system
        util.save_entry(title, text)

        # redirect to new page
        return HttpResponseRedirect(f"/wiki/{title}")

    # if Get show page with form
    return render(request, "encyclopedia/create.html", {
        "form": newpage()
    })

def edit(request):
    """edit page"""
    if request.method == "POST":

        # when get true value display the page
        if request.POST.get("edit") == "true":
            title = request.POST.get("title")
            
            # get page content
            text = util.get_entry(title)

            # render edit page
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "text": text
            })

        # else edit page
        else:
            
            # get the form from user
            form = newpage(request.POST)

            # check if form is valid
            if form.is_valid():

                # get data from user
                title = form.cleaned_data["title"]
                text = form.cleaned_data["text"]

                # update page in system
                util.save_entry(title, text)

                # redirect user to new page
                return HttpResponseRedirect(f"/wiki/{title}")

def random(request):
    """display random page"""

    # get list of all entries
    l = util.list_entries()

    # redirect to random page
    return HttpResponseRedirect(f"wiki/{choice(l)}")
    



