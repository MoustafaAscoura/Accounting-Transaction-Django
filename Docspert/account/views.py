from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Account
from .reader import open_file_and_load_content_into_database, UnsupportedFileExtension, UnsupportedFileFormat
from .forms import TransactionForm


def index(request):
    if request.method == "GET":
        query = request.GET.get("query")
        if query:
            accounts = Account.find_accounts_by_query(query)
        else:
            accounts = Account.get_all_objects()

        # Get Accounts matching the query
        context = {
            "accounts": accounts,
            "query": query or ""
        }

    elif request.method == "POST":
        file = request.FILES.get("accounts_file")
        try:
            failed_docs = open_file_and_load_content_into_database(file)
            if failed_docs:
                context = {
                    "file_upload_success": False,
                    "message": "Some accounts were not imported successfully"
                }
            else:
                context = {
                    "file_upload_success": True,
                    "message": "Accounts imported successfully"
                }

        except UnsupportedFileExtension as err:
            context = {
                "file_upload_success": False,
                "message": str(err)
            }

        except UnsupportedFileFormat as err:
            context = {
                "file_upload_success": False,
                "message": str(err)
            }

        except Exception as e:
            context = {
                "file_upload_success": False,
                "message": "File not valid"
            }

        finally:
            context["accounts"] = Account.get_all_objects()
    else:
        return HttpResponseBadRequest("Method not allowed")

    return render(request, "index.html", context=context)


def details(request, account_id: str):
    if request.method == "POST":
        print(request.POST)
        transaction_form = TransactionForm(request.POST)
        transaction_form.save()

    account = get_object_or_404(Account, pk=account_id)
    context = {
        "account": account,
        "transaction_form": TransactionForm(),
    }
    return render(request, "details.html", context=context)
