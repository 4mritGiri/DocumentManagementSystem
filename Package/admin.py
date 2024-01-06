import json
from django.urls import reverse
from django.contrib import admin
from .models import Document, StoreRoom, Compartment, Package, Branch, PackageVerification, Rack
from django.utils.html import mark_safe # type: ignore
from .utils import generate_qr

# Register your models here.
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('doc_type', 'doc_id', 'doc_classification_type', 'doc_details')
    list_filter = ('doc_classification_type', 'doc_type')
    search_fields = ('doc_id', 'doc_classification_type', 'doc_type', 'doc_details')

    fieldsets = (
        ('Document', {
            'fields': ('doc_type', 'doc_classification_type')
        }),
        (
            'Document Details', {
                'fields': ('doc_details',),
                'classes': ('collapse',)
            }
        )
    )

# Branch
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('branch_name', 'branch_id', 'branch_code', 'branch_location')
    list_filter = ('branch_name', 'branch_code', 'branch_location')
    search_fields = ('branch_id', 'branch_name', 'branch_code', 'branch_location')

    fieldsets = (
        ('Branch', {
            'fields': ('branch_name', 'branch_code', 'branch_location')
        }),
    )

# Compartment
@admin.register(Compartment)
class CompartmentAdmin(admin.ModelAdmin):
    list_display = ('compartment_name', 'compartment_id', 'compartment_location')
    list_filter = ('compartment_name', 'compartment_location')
    search_fields = ('compartment_id', 'compartment_name', 'compartment_location')

    fieldsets = (
        ('Compartment', {
            'fields': ('compartment_name', 'compartment_location')
        }),
    )


# Rack
@admin.register(StoreRoom)
class StoreRoomAdmin(admin.ModelAdmin):
    list_display = ('room', 'room_id', 'room_location')
    list_filter = ('store_room_name', 'store_room_id')
    search_fields = ('store_room_id', 'store_room_name')

    def room(self, obj):
        return obj.store_room_name
    
    def room_id(self, obj):
        return obj.store_room_id
    
    def room_location(self, obj):
        return obj.rack.rack_name + ', ' + obj.branch.branch_name
    
    def get_queryset(self, request):
        qs = super(StoreRoomAdmin, self).get_queryset(request)
        return qs.select_related('rack', 'branch')
    
    fieldsets = (
        ('Store Room', {
            'fields': ('store_room_name', 'rack', 'branch')
        }),
    )
    

# Rack
@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ('rack_name', 'rack_id', 'rack_location')
    list_filter = ('rack_name', 'rack_id')
    search_fields = ('rack_id', 'rack_name')

    def rack_name(self, obj):
        return obj.rack_name
    
    def rack_id(self, obj):
        return obj.rack_id
    
    def rack_location(self, obj):
        return obj.compartment.compartment_name + ', ' + obj.compartment.compartment_location
    
    fieldsets = (
        ('Rack', {
            'fields': ('rack_name', 'compartment')
        }),
    )

# Register your models here.
@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('pkg_name', 'document', 'details', 'packaging_size', 'status', 'destruction_eligible_time', 'qr_code','condition', 'created_at', 'updated_at', 'remarks')

    def document(self, obj):
        return obj.document_type.doc_type
    
    def qr_code(self, obj):
        # Generate QR code and get the path
        qr_code_path = f"./media/qr_codes/{obj.pkg_id}_qr_code.png"

        data = {
            "PackageID": obj.pkg_id,
            "PackageName": obj.pkg_name,
            "DocumentType": obj.document_type.doc_type,
            "Details": obj.details,
            "PackagingSize": obj.packaging_size,
            "Status": obj.status,
            "DestructionEligibleTime": str(obj.destruction_eligible_time),
            "Remarks": obj.remarks
        }
        json_data = json.dumps(data)
        
        generate_qr(json_data, output_path=qr_code_path)
        
        
        return mark_safe(f'''
            <div style="display:flex; flex-direction: row; align-items: center;">
                <a href="#" onclick="openPopup('../../../../../{qr_code_path}'); return false;">
                    <img src="../../../../../{qr_code_path}" alt="{obj.pkg_name}" width="65" height="65" />
                </a>
                <div>
                    <a
                      download="../../../../../{qr_code_path}"
                      href="../../../../../{qr_code_path}"
                      class="btn btn-primary btn-sm justify-content-center ml-1"
                    >
                        <i class="fa fa-download"></i>
                    </a>
                    <div style="padding-vertival: 3px;border-radius: 2px; cursor: pointer;" class="bg-success ml-1 mt-1" onclick="printPage('../../../../../{qr_code_path}')">Print</div>
                </div>
                <script>
                    // Get the screen width and height
                    var screenWidth = window.screen.width;
                    var screenHeight = window.screen.height;

                    // Calculate the center position
                    var centerX = (screenWidth) / 2; 
                    var centerY = (screenHeight - screenHeight/2 ) / 2; 

                    function openPopup(imagePath) {{
                        // Open the window in the center
                        window.open(imagePath, 'Image Pop-up', `width=400,height=400,left=${{centerX}},top=${{centerY}}`);
                    }}
                    function printPage(qrCodePath) {{
                        var popupWindow = window.open('', 'Image Pop-up',  `width=550,height=500,left=${{centerX}},top=${{centerY-50}}`);

                        // Set the content of the new window
                        popupWindow.document.write(`
                            <html>
                                <head>
                                    <title>QR Code</title>
                                </head>
                                <body style="display:flex; flex-direction: column;">
                                    <h2 style="text-align: center; color: #0062cc;">Document Management System</h2>
                                    <div style="display:flex; flex-direction: row; margin:0 auto;">
                                        <img src="${{qrCodePath}}" alt="QR Code" width="200" height="200" />
                                        <table style="text-align: left;" class="table table-bordered table-sm">
                                            <tr >
                                                <th>Package ID :</th>
                                                <td>{obj.pkg_id}</td>
                                            </tr>
                                            <tr>
                                                <th>Package Name :</th>
                                                <td>{obj.pkg_name}</td>
                                            </tr>
                                            <tr>
                                                <th>Document Type :</th>
                                                <td>{obj.document_type.doc_type}</td>
                                            </tr>
                                            <tr>
                                                <th>Details :</th>
                                                <td>{obj.details}</td>
                                            </tr>
                                            <tr>
                                                <th>Packaging Size :</th>
                                                <td>{obj.packaging_size}</td>
                                            </tr>
                                            <tr>
                                                <th>Status :</th>
                                                <td>{obj.status}</td>
                                            </tr>
                                            <tr>
                                                <th>Destruction Eligible Time :</th>
                                                <td>{obj.destruction_eligible_time}</td>
                                            </tr>
                                            <tr>
                                                <th>Remarks :</th>
                                                <td>{obj.remarks}</td>
                                            </tr>
                                        </table>
                                    </div>
                                    <p style="text-align: center;"><span style="color: #967000;">Note:-</span>Scan The qr code to complain your package condition.</p>
                                </body>
                            </html>
                        `);

                        popupWindow.document.close();

                        // Wait for the content to be loaded before printing
                        popupWindow.onload = function () {{
                            if (popupWindow.document.readyState === "complete") {{
                                // Print the window content
                                popupWindow.print();
                            }} else {{
                                console.error("Failed to load content for printing.");
                            }}
                        }};
                    }}


                </script>
            </div>
        ''')

    qr_code.short_description = "QR Code" 
    readonly_fields = ['qr_code', 'status']

    fieldsets = (
        ('Package', {
            'fields': ('pkg_name', 'document_type', 'details')
        }),
        (
            'Package Details', {
                'fields': ('packaging_size', 'destruction_eligible_time', 'remarks','status'),
                # 'classes': ('collapse',)
            }
        ),
        (
            'QR Code', {
                'fields': ('condition','qr_code',),
                'classes': ('collapse',)
            }
        )
    )


# Package verification
@admin.register(PackageVerification)
class PackageVerificationAdmin(admin.ModelAdmin):
    list_display = ('package', 'authorizer', 'status', 'verification_remarks', 'verification_date')
    
    def package(self, obj):
        return obj.package_id.pkg_name
    
    def authorizer(self, obj):
        return obj.authorizer.username
    
    def statu(self, obj):
        return obj.status.status
    
    fieldsets = (
        ('Package Verification', {
            'fields': ('package', 'authorizer', 'verification_remarks')
        }),
        (
            'Package Verification Status', {
                'fields': ('status', 'verification_date'),
                # 'classes': ('collapse',)
            }
        )
    )
    
    