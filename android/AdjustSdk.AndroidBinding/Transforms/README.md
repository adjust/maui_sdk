# Android Binding Metadata Transformations

This directory contains XML metadata files that transform the Java binding generation process for the Adjust Android SDK.

## Purpose

The `Metadata.xml` file customizes how the Xamarin/MAUI Android binding generator processes the Java AAR files. This is necessary because:

1. **The Android SDK is obfuscated/minified** - Contains synthetic classes and methods that don't need to be exposed
2. **Internal implementation details** - Some classes/interfaces are internal and shouldn't be part of the public API
3. **Binding conflicts** - Some Java patterns don't translate well to C# and need to be excluded

## Current Build Status

The binding builds successfully with **11 warnings** and **0 errors**.

### Expected Warnings

These warnings are **expected and acceptable** - they result from intentionally removing internal implementation classes:

| Warning Code | Description | Reason |
|-------------|-------------|--------|
| **BG8605** (2x) | Java types `$` and `Callable<V>` not found | Consequence of removing the internal scheduler package |
| **BG8606** (1x) | Resolution report available | General notice about types that couldn't be bound |
| **BG8604** (1x) | Missing ancestor `AdjustFactory` for nested type | Parent class removed as it's internal |
| **BG8800** (1x) | Unknown parameter type `ReferrerDetails` | Type removed as it's internal |
| **BG8503** (1x) | Invalidating `IInstallReferrerReadListener` | Interface invalidated due to missing `ReferrerDetails` |

**These warnings do not affect the public API or cause compilation errors.**

## Metadata Rules Explained

### 1. Remove Internal Network Package
```xml
<remove-node path="/api/package[@name='com.adjust.sdk.network']" />
<remove-node path="/api/package[@name='com.adjust.sdk.scheduler']" />
```
**Why:** These packages contain internal HTTP and threading implementation details not needed in the MAUI wrapper.

### 2. Remove Specific Public Methods Not Needed
```xml
<remove-node path="/api/package[@name='com.adjust.sdk']/class[@name='Adjust']/method[
  @name='getDefaultInstance' or @name='getGooglePlayInstallReferrer']" />
```
**Why:** These methods are for internal use or deprecated functionality not exposed in the MAUI API.

### 3. Remove Internal Handler Interfaces/Classes
```xml
<remove-node path="/api/package[@name='com.adjust.sdk']/interface[
  @name='IAttributionHandler' or
  @name='IPackageHandler' or
  @name='IPurchaseVerificationHandler' or
  @name='ISdkClickHandler' or
  @name='IActivityHandler' or
  @name='ILogger']" />
```
**Why:** These are internal architecture interfaces not part of the public API. They depend on removed packages.

### 4. Remove Internal Implementation Classes
```xml
<remove-node path="/api/package[@name='com.adjust.sdk']/class[
  @name='PackageBuilder' or
  @name='Logger' or
  @name='Reflection' or ...]" />
```
**Why:** These are internal implementation classes that users should never interact with directly.

### 5. Remove Internal Data Classes
```xml
<remove-node path="/api/package[@name='com.adjust.sdk']/class[contains(@name, 'ResponseData')]" />
```
**Why:** Response data classes are used internally for network communication and are not part of the public API.

### 6. Remove Obfuscated Nested Types
```xml
<remove-node path="/api/package[@name='com.adjust.sdk']/class[starts-with(@name, 'ActivityHandler.')]" />
```
**Why:** The Android SDK is obfuscated, creating synthetic nested classes like `ActivityHandler.1`, `ActivityHandler.2`, etc. These are:
- Lambda/anonymous class artifacts with no meaningful names
- Not bindable (missing parent type after obfuscation)
- Not part of the public API

**Similar rules exist for:** `AttributionHandler`, `PackageHandler`, `PurchaseVerificationHandler`, `SdkClickHandler`, `AdjustInstance`, `InstallReferrer`, `AdjustLinkResolution`, `Util`, `GooglePlayServicesClient`, `DeviceInfo`, `PackageBuilder`

## Build Process

When the Android binding project builds:

1. **Extract AAR** - The `.aar` files are extracted from `libs/`
2. **Parse Java API** - The binding generator creates an `api.xml` from the Java bytecode
3. **Apply Metadata** - Transformations from `Metadata.xml` are applied to remove unwanted types
4. **Generate C#** - C# wrapper classes are generated for the remaining public API
5. **Compile** - The C# code is compiled into the binding DLL

## Maintenance

### When to Update Metadata.xml

Update this file when:
- **New SDK version** introduces new internal classes that cause binding errors
- **Build errors occur** due to missing or conflicting types
- **New warnings appear** that indicate internal types being exposed
- **Public API changes** require exposing previously hidden types

### Testing Changes

After modifying `Metadata.xml`:

1. **Clean build artifacts:**
   ```bash
   rm -rf .artifacts/AdjustSdk.AndroidBinding
   ```

2. **Rebuild the binding:**
   ```bash
   dotnet build android/AdjustSdk.AndroidBinding/AdjustSdk.AndroidBinding.csproj --configuration Debug
   ```

3. **Verify the build:**
   - Check for 0 errors
   - Confirm warnings are expected (see table above)
   - Ensure public API classes are still generated

4. **Test the binding:**
   - Build a consuming project to ensure the public API is accessible
   - Verify that internal classes are not exposed

### Debugging Binding Issues

If you encounter binding issues:

1. **Check the resolution report:**
   ```bash
   cat .artifacts/AdjustSdk.AndroidBinding/obj/Debug/net8.0-android34.0/net8.0-android34.0/java-resolution-report.log
   ```

2. **Review the parsed API:**
   ```bash
   cat .artifacts/AdjustSdk.AndroidBinding/obj/Debug/net8.0-android34.0/net8.0-android34.0/api.xml
   ```

3. **Examine generated C# code:**
   ```bash
   ls .artifacts/AdjustSdk.AndroidBinding/obj/Debug/net8.0-android34.0/net8.0-android34.0/generated/src/
   ```

4. **Check what got removed:**
   ```bash
   cat .artifacts/AdjustSdk.AndroidBinding/obj/Debug/net8.0-android34.0/net8.0-android34.0/api.xml.fixed
   ```

### Common Patterns

When adding new removal rules:

- **Remove entire class:** `<remove-node path="/api/package[@name='X']/class[@name='Y']" />`
- **Remove obfuscated nested types:** `<remove-node path="...class[starts-with(@name, 'Parent.')]" />`
- **Remove specific methods:** `<remove-node path=".../class[@name='X']/method[@name='Y']" />`
- **Remove multiple classes:** Use `@name='A' or @name='B' or @name='C'`

**Important:** Avoid removing classes that have obfuscated nested types. Remove the entire parent class instead to prevent "missing ancestor" warnings.

## XPath Reference

Common XPath patterns used in `Metadata.xml`:

| Pattern | Matches |
|---------|---------|
| `@name='ClassName'` | Exact class name |
| `starts-with(@name, 'Prefix.')` | Names starting with prefix (e.g., nested types) |
| `contains(@name, 'Text')` | Names containing text |
| `@name='A' or @name='B'` | Multiple exact matches |
| `/class[@name='X']/method[@name='Y']` | Specific method in class |

## References

- [Xamarin Android Binding Metadata](https://learn.microsoft.com/en-us/xamarin/android/platform/binding-java-library/customizing-bindings/java-bindings-metadata)
- [Binding Java Libraries](https://learn.microsoft.com/en-us/xamarin/android/platform/binding-java-library/)
- [XPath Syntax](https://www.w3.org/TR/xpath-10/)
