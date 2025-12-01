#!/usr/bin/env python3
"""
OpenAPI Normalizer Script

This script normalizes an OpenAPI specification file to comply with OpenAPI 3.0+ requirements.
It fixes common validation errors such as:
- Invalid map names (spaces in schema names)
- Enum type mismatches
- Missing required fields (like license name)
- Property names that don't comply with JSON schema requirements

Usage:
    python normalize_openapi.py input_file.json [options]

Examples:
    # Output to stdout (default)
    python normalize_openapi.py integration.json
    
    # Output to specific file
    python normalize_openapi.py integration.json --output-file output.json
    
    # Explicit stdout (same as default)
    python normalize_openapi.py integration.json --output-file -
    
    # With custom schema renames
    python normalize_openapi.py integration.json --rename "Error Message:ErrorMessage"
    
    # Filter endpoints by tags
    python normalize_openapi.py integration.json --filter-tags "WiFi Broadcasts" "Networks"
    
    # Multiple custom renames with custom output
    python normalize_openapi.py integration.json --rename "Error Message:ErrorMessage" --output-file result.json

Options:
    --rename OLD_NAME:NEW_NAME    Replace a schema name (case sensitive, can be used multiple times)
    --output-file FILE            Output file path (use '-' for stdout, default: stdout)
    --filter-tags TAG [TAG ...]   Only include endpoints with these tags (can specify multiple tags)
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List


def normalize_schema_name(name: str) -> str:
    """
    Normalize a schema name to match the regex ^[a-zA-Z0-9\\.\\-_]+$
    
    Replaces spaces with underscores and removes any other invalid characters.
    
    Args:
        name: The original schema name
        
    Returns:
        The normalized schema name
    """
    # Replace spaces with underscores
    normalized = name.replace(" ", "_")
    # Remove any characters that don't match the allowed pattern
    normalized = re.sub(r'[^a-zA-Z0-9.\-_]', '', normalized)
    return normalized


def walk_and_fix_properties(obj: Any, property_fixes: Dict[str, Dict[str, Any]]) -> Any:
    """
    Recursively walk the spec and replace matching properties.
    
    This mimics jq's walk function, replacing entire property definitions
    when a matching property name is found.
    
    Args:
        obj: The object to walk (can be dict, list, or primitive)
        property_fixes: Dictionary mapping property names to their new definitions
                       e.g., {'frequencyGHz': {'type': 'number', 'format': 'double'}}
        
    Returns:
        The modified object
    """
    if isinstance(obj, dict):
        # Check if this dict has any of the properties to fix
        for prop_name, new_definition in property_fixes.items():
            if prop_name in obj:
                # Replace the entire property definition
                obj[prop_name] = new_definition.copy()
        
        # Recursively process all values
        for key, value in obj.items():
            obj[key] = walk_and_fix_properties(value, property_fixes)
    
    elif isinstance(obj, list):
        # Recursively process all items
        return [walk_and_fix_properties(item, property_fixes) for item in obj]
    
    return obj


def fix_integer_enum_values(obj: Any) -> Any:
    """
    Recursively walk the spec and convert enum values to numbers for integer type schemas.
    
    This mimics the second jq walk: converting enum values to match integer types.
    
    Args:
        obj: The object to walk (can be dict, list, or primitive)
        
    Returns:
        The modified object
    """
    if isinstance(obj, dict):
        # Check if this is an integer type with enum array
        if obj.get('type') == 'integer' and 'enum' in obj and isinstance(obj['enum'], list):
            # Convert enum values to numbers
            try:
                obj['enum'] = [int(float(v)) if not isinstance(v, (int, float)) else int(v) 
                              for v in obj['enum']]
            except (ValueError, TypeError):
                # Keep original if conversion fails
                pass
        
        # Recursively process all values
        for key, value in obj.items():
            obj[key] = fix_integer_enum_values(value)
    
    elif isinstance(obj, list):
        # Recursively process all items
        return [fix_integer_enum_values(item) for item in obj]
    
    return obj


def fix_enum_type_mismatch(schema: Dict[str, Any]) -> None:
    """
    Fix enum type mismatches by converting enum values to match the type field.
    
    Recursively processes all properties in the schema.
    
    Args:
        schema: The schema dictionary to fix
    """
    if not isinstance(schema, dict):
        return
    
    # If this schema has both type and enum, ensure they match
    if 'type' in schema and 'enum' in schema:
        schema_type = schema['type']
        enum_values = schema['enum']
        
        if schema_type == 'integer':
            # Convert string enum values to integers
            fixed_enum = []
            for value in enum_values:
                if isinstance(value, str):
                    try:
                        fixed_enum.append(int(value))
                    except (ValueError, TypeError):
                        # If conversion fails, try float then int
                        try:
                            fixed_enum.append(int(float(value)))
                        except (ValueError, TypeError):
                            # Keep original if conversion fails
                            fixed_enum.append(value)
                else:
                    fixed_enum.append(value)
            schema['enum'] = fixed_enum
        elif schema_type == 'number':
            # Convert string enum values to numbers
            fixed_enum = []
            for value in enum_values:
                if isinstance(value, str):
                    try:
                        fixed_enum.append(float(value))
                    except (ValueError, TypeError):
                        # Keep original if conversion fails
                        fixed_enum.append(value)
                else:
                    fixed_enum.append(value)
            schema['enum'] = fixed_enum
        elif schema_type == 'string':
            # Convert numeric enum values to strings
            schema['enum'] = [str(v) if not isinstance(v, str) else v for v in enum_values]
    
    # Recursively process properties
    if 'properties' in schema:
        for prop_name, prop_schema in schema['properties'].items():
            fix_enum_type_mismatch(prop_schema)
    
    # Process items for arrays
    if 'items' in schema:
        fix_enum_type_mismatch(schema['items'])
    
    # Process allOf, anyOf, oneOf
    for key in ['allOf', 'anyOf', 'oneOf']:
        if key in schema:
            for sub_schema in schema[key]:
                fix_enum_type_mismatch(sub_schema)


def update_schema_references(obj: Any, name_mapping: Dict[str, str]) -> None:
    """
    Update all $ref references to use the new normalized schema names.
    
    Args:
        obj: The object to update (can be dict, list, or primitive)
        name_mapping: Dictionary mapping old names to new names
    """
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == '$ref' and isinstance(value, str):
                # Extract the schema name from the reference
                if value.startswith('#/components/schemas/'):
                    old_name = value.replace('#/components/schemas/', '')
                    if old_name in name_mapping:
                        obj[key] = f'#/components/schemas/{name_mapping[old_name]}'
            elif key == 'mapping' and isinstance(value, dict):
                # Handle discriminator mappings - these also contain schema references
                for map_key, map_value in value.items():
                    if isinstance(map_value, str) and map_value.startswith('#/components/schemas/'):
                        old_name = map_value.replace('#/components/schemas/', '')
                        if old_name in name_mapping:
                            value[map_key] = f'#/components/schemas/{name_mapping[old_name]}'
            else:
                update_schema_references(value, name_mapping)
    elif isinstance(obj, list):
        for item in obj:
            update_schema_references(item, name_mapping)


def fix_x_tags_fields(obj: Any) -> None:
    """
    Fix x-tags fields that are strings and should be arrays.
    
    Args:
        obj: The object to fix (can be dict, list, or primitive)
    """
    if isinstance(obj, dict):
        for key, value in list(obj.items()):
            if key == 'x-tags' and isinstance(value, str):
                # Convert string to array with single element
                obj[key] = [value]
            else:
                fix_x_tags_fields(value)
    elif isinstance(obj, list):
        for item in obj:
            fix_x_tags_fields(item)


def filter_endpoints_by_tags(spec: Dict[str, Any], allowed_tags: List[str], verbose: bool = True) -> None:
    """
    Remove all endpoints that don't have at least one of the allowed tags.
    
    Args:
        spec: The OpenAPI specification dictionary
        allowed_tags: List of tags to keep (endpoints must have at least one)
        verbose: Whether to print progress messages
    """
    if not allowed_tags or 'paths' not in spec:
        return
    
    # Convert to set for faster lookup
    allowed_tags_set = set(allowed_tags)
    
    paths_to_remove = []
    endpoints_removed = 0
    endpoints_kept = 0
    
    for path, path_item in spec['paths'].items():
        if not isinstance(path_item, dict):
            continue
        
        operations_to_remove = []
        
        for method, operation in path_item.items():
            # Skip non-operation keys
            if method not in ['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace']:
                continue
            
            if not isinstance(operation, dict):
                continue
            
            # Check if operation has any of the allowed tags
            operation_tags = operation.get('tags', [])
            if not any(tag in allowed_tags_set for tag in operation_tags):
                operations_to_remove.append(method)
                endpoints_removed += 1
            else:
                endpoints_kept += 1
        
        # Remove operations that don't match
        for method in operations_to_remove:
            del path_item[method]
        
        # If all operations removed, mark path for removal
        has_operations = any(key in ['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace'] 
                            for key in path_item.keys())
        if not has_operations:
            paths_to_remove.append(path)
    
    # Remove empty paths
    for path in paths_to_remove:
        del spec['paths'][path]
    
    if verbose:
        print(f"  Kept {endpoints_kept} endpoints, removed {endpoints_removed} endpoints")
        print(f"  Removed {len(paths_to_remove)} empty paths")


def find_referenced_schemas(obj: Any, referenced: set) -> None:
    """
    Recursively find all schema references in an object.
    
    Args:
        obj: The object to search (can be dict, list, or primitive)
        referenced: Set to store referenced schema names
    """
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == '$ref' and isinstance(value, str):
                # Extract schema name from reference
                if value.startswith('#/components/schemas/'):
                    schema_name = value.replace('#/components/schemas/', '')
                    referenced.add(schema_name)
            elif key == 'mapping' and isinstance(value, dict):
                # Handle discriminator mappings - these also contain schema references
                for map_key, map_value in value.items():
                    if isinstance(map_value, str) and map_value.startswith('#/components/schemas/'):
                        schema_name = map_value.replace('#/components/schemas/', '')
                        referenced.add(schema_name)
            else:
                find_referenced_schemas(value, referenced)
    elif isinstance(obj, list):
        for item in obj:
            find_referenced_schemas(item, referenced)


def remove_unused_schemas(spec: Dict[str, Any], verbose: bool = True) -> None:
    """
    Remove schemas that are not referenced anywhere in the spec.
    
    Args:
        spec: The OpenAPI specification dictionary
        verbose: Whether to print progress messages
    """
    if 'components' not in spec or 'schemas' not in spec['components']:
        return
    
    schemas = spec['components']['schemas']
    original_count = len(schemas)
    
    # Find all referenced schemas
    referenced_schemas = set()
    
    # Search in paths
    if 'paths' in spec:
        find_referenced_schemas(spec['paths'], referenced_schemas)
    
    # Search in components (excluding schemas themselves to avoid circular refs initially)
    for component_type, components in spec.get('components', {}).items():
        if component_type != 'schemas':
            find_referenced_schemas(components, referenced_schemas)
    
    # Now iteratively find schemas referenced by other schemas
    # Keep iterating until no new schemas are found
    while True:
        new_schemas = set()
        for schema_name in referenced_schemas:
            if schema_name in schemas:
                find_referenced_schemas(schemas[schema_name], new_schemas)
        
        # If no new schemas found, we're done
        new_refs = new_schemas - referenced_schemas
        if not new_refs:
            break
        referenced_schemas.update(new_refs)
    
    # Remove unreferenced schemas
    schemas_to_remove = set(schemas.keys()) - referenced_schemas
    for schema_name in schemas_to_remove:
        del schemas[schema_name]
    
    if verbose and schemas_to_remove:
        print(f"  Removed {len(schemas_to_remove)} unused schemas ({original_count} -> {len(schemas)})")


def add_security_to_operations(spec: Dict[str, Any], verbose: bool = True) -> None:
    """
    Add security definitions to all operations that don't have them.
    
    If there's a security scheme defined in components/securitySchemes,
    we'll reference it. Otherwise, we'll add an empty security array.
    
    Args:
        spec: The OpenAPI specification dictionary
        verbose: Whether to print progress messages
    """
    # Check if there are any security schemes defined
    security_schemes = spec.get('components', {}).get('securitySchemes', {})
    
    # Determine what security to add
    if security_schemes:
        # Use the first security scheme found
        first_scheme = list(security_schemes.keys())[0]
        default_security = [{first_scheme: []}]
    else:
        # Add empty security (means no authentication required)
        default_security = []
    
    # Add security to all operations
    if 'paths' in spec:
        operations_fixed = 0
        for path, path_item in spec['paths'].items():
            if isinstance(path_item, dict):
                for method, operation in path_item.items():
                    # Skip non-operation keys like 'parameters', 'servers', etc.
                    if method in ['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace']:
                        if isinstance(operation, dict) and 'security' not in operation:
                            operation['security'] = default_security
                            operations_fixed += 1
        
        if operations_fixed > 0 and verbose:
            print(f"  Added security to {operations_fixed} operations")


def normalize_openapi_spec(spec: Dict[str, Any], custom_renames: Dict[str, str] = None, 
                          filter_tags: List[str] = None, type_fixes: List[tuple] = None,
                          verbose: bool = True) -> Dict[str, Any]:
    """
    Normalize an OpenAPI specification to comply with OpenAPI 3.0+ requirements.
    
    Args:
        spec: The OpenAPI specification dictionary
        custom_renames: Optional dictionary of custom schema name replacements (old_name -> new_name)
        filter_tags: Optional list of tags to filter endpoints by
        type_fixes: Optional list of tuples (property_name, new_type) to fix property types
        verbose: Whether to print progress messages
        
    Returns:
        The normalized specification
    """
    # Create a deep copy to avoid modifying the original
    import copy
    normalized_spec = copy.deepcopy(spec)
    
    if custom_renames is None:
        custom_renames = {}
    
    # Filter endpoints by tags first (before other processing)
    if filter_tags:
        if verbose:
            print(f"Filtering endpoints by tags: {', '.join(filter_tags)}")
        filter_endpoints_by_tags(normalized_spec, filter_tags, verbose)
        # Remove schemas that are no longer referenced after filtering
        if verbose:
            print("Removing unused schemas...")
        remove_unused_schemas(normalized_spec, verbose)
    
    # Fix 1: Add license name if missing
    if 'info' in normalized_spec:
        if 'license' in normalized_spec['info']:
            if not normalized_spec['info']['license'].get('name'):
                normalized_spec['info']['license']['name'] = 'Proprietary'
        else:
            normalized_spec['info']['license'] = {
                'name': 'Proprietary'
            }
    
    # Fix 2: Normalize schema names and create mapping
    if 'components' in normalized_spec and 'schemas' in normalized_spec['components']:
        schemas = normalized_spec['components']['schemas']
        name_mapping = {}
        new_schemas = {}
        
        for old_name, schema in schemas.items():
            # First check if there's a custom rename
            if old_name in custom_renames:
                new_name = custom_renames[old_name]
                if verbose:
                    print(f"Custom rename: '{old_name}' -> '{new_name}'")
            else:
                new_name = normalize_schema_name(old_name)
                if new_name != old_name and verbose:
                    print(f"Auto-normalizing schema: '{old_name}' -> '{new_name}'")
            
            if new_name != old_name:
                name_mapping[old_name] = new_name
            
            new_schemas[new_name] = schema
        
        # Replace the schemas with normalized names
        normalized_spec['components']['schemas'] = new_schemas
        
        # Update all references throughout the spec
        if name_mapping:
            if verbose:
                print(f"\nUpdating {len(name_mapping)} schema references throughout the spec...")
            update_schema_references(normalized_spec, name_mapping)
    
    # Fix 3: Fix property types that don't match API behavior (walk-based replacement)
    if type_fixes:
        if verbose:
            print("\nFixing property types to match API behavior...")
        
        # Convert type_fixes list to property_fixes dict
        property_fixes = {}
        for property_name, new_type in type_fixes:
            if new_type == 'number':
                property_fixes[property_name] = {'type': 'number', 'format': 'double'}
            elif new_type == 'integer':
                property_fixes[property_name] = {'type': 'integer', 'format': 'int32'}
            elif new_type == 'string':
                property_fixes[property_name] = {'type': 'string'}
            elif new_type == 'boolean':
                property_fixes[property_name] = {'type': 'boolean'}
            
            if verbose:
                print(f"  Will replace all '{property_name}' properties with: {property_fixes[property_name]}")
        
        # Walk the entire spec and replace matching properties
        normalized_spec = walk_and_fix_properties(normalized_spec, property_fixes)
        
        if verbose:
            print(f"  Completed property replacement walk")
    
    # Fix 4: Convert enum values to numbers for integer types
    if verbose:
        print("\nFixing integer enum values...")
    normalized_spec = fix_integer_enum_values(normalized_spec)
    if verbose:
        print("  Completed integer enum conversion")
    
    # Fix 4: Convert enum values to numbers for integer types
    if verbose:
        print("\nFixing integer enum values...")
    normalized_spec = fix_integer_enum_values(normalized_spec)
    if verbose:
        print("  Completed integer enum conversion")
    
    # Fix 5: Fix enum type mismatches in all schemas
    if 'components' in normalized_spec and 'schemas' in normalized_spec['components']:
        if verbose:
            print("\nFixing enum type mismatches...")
        for schema_name, schema in normalized_spec['components']['schemas'].items():
            fix_enum_type_mismatch(schema)
    
    # Fix 6: Also fix enum type mismatches in path parameters and request/response bodies
    if 'paths' in normalized_spec:
        for path, path_item in normalized_spec['paths'].items():
            if isinstance(path_item, dict):
                for method, operation in path_item.items():
                    if isinstance(operation, dict):
                        # Fix in parameters
                        if 'parameters' in operation:
                            for param in operation['parameters']:
                                if 'schema' in param:
                                    fix_enum_type_mismatch(param['schema'])
                        
                        # Fix in request body
                        if 'requestBody' in operation:
                            fix_enum_type_mismatch(operation['requestBody'])
                        
                        # Fix in responses
                        if 'responses' in operation:
                            for response in operation['responses'].values():
                                fix_enum_type_mismatch(response)
    
    # Fix 7: Fix x-tags fields that should be arrays
    if verbose:
        print("\nFixing x-tags fields...")
    fix_x_tags_fields(normalized_spec)
    
    # Fix 8: Add security to operations that are missing it
    if verbose:
        print("\nAdding security definitions to operations...")
    add_security_to_operations(normalized_spec, verbose)
    
    return normalized_spec


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Normalize an OpenAPI specification to comply with OpenAPI 3.0+ requirements.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Output to stdout (default)
  %(prog)s integration.json
  
  # Output to specific file
  %(prog)s integration.json --output-file output.json
  
  # Explicit stdout
  %(prog)s integration.json --output-file -
  
  # Filter endpoints by tags
  %(prog)s integration.json --filter-tags "WiFi Broadcasts" "Networks"
  
  # With custom schema renames (case sensitive)
  %(prog)s integration.json --rename "Error Message:ErrorMessage" --output-file result.json
  
  # Fix property types to match API behavior
  %(prog)s integration.json --fix-type "frequencyGHz:number" --output-file result.json
        """
    )
    
    parser.add_argument('input_file', help='Input OpenAPI JSON file')
    parser.add_argument(
        '--rename',
        action='append',
        metavar='OLD_NAME:NEW_NAME',
        help='Replace a schema name (case sensitive, can be used multiple times)'
    )
    parser.add_argument(
        '--output-file',
        metavar='FILE',
        help='Output file path (use "-" for stdout, default: stdout)'
    )
    parser.add_argument(
        '--filter-tags',
        nargs='+',
        metavar='TAG',
        help='Only include endpoints with these tags (can specify multiple tags)'
    )
    parser.add_argument(
        '--fix-type',
        action='append',
        metavar='PROPERTY:TYPE',
        help='Fix property type (e.g., "frequencyGHz:number", can be used multiple times)'
    )
    
    args = parser.parse_args()
    
    input_file = Path(args.input_file)
    
    if not input_file.exists():
        print(f"Error: Input file '{input_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    # Determine output destination (default is stdout)
    output_to_stdout = not args.output_file or args.output_file == '-'
    if args.output_file and args.output_file != '-':
        output_file = Path(args.output_file)
    else:
        output_file = None  # stdout
    
    # Parse custom renames
    custom_renames = {}
    if args.rename:
        for rename_pair in args.rename:
            if ':' not in rename_pair:
                print(f"Error: Invalid rename format '{rename_pair}'. Expected format: 'OLD_NAME:NEW_NAME'", file=sys.stderr)
                sys.exit(1)
            old_name, new_name = rename_pair.split(':', 1)
            custom_renames[old_name] = new_name
        
        if not output_to_stdout:
            print(f"Custom renames specified: {len(custom_renames)}")
            for old, new in custom_renames.items():
                print(f"  '{old}' -> '{new}'")
            print()
    
    # Parse type fixes
    type_fixes = []
    if args.fix_type:
        for fix_pair in args.fix_type:
            if ':' not in fix_pair:
                print(f"Error: Invalid fix-type format '{fix_pair}'. Expected format: 'PROPERTY:TYPE'", file=sys.stderr)
                sys.exit(1)
            property_name, new_type = fix_pair.split(':', 1)
            if new_type not in ['string', 'number', 'integer', 'boolean']:
                print(f"Error: Invalid type '{new_type}'. Must be one of: string, number, integer, boolean", file=sys.stderr)
                sys.exit(1)
            type_fixes.append((property_name, new_type))
        
        if not output_to_stdout:
            print(f"Property type fixes specified: {len(type_fixes)}")
            for prop, typ in type_fixes:
                print(f"  '{prop}' -> {typ}")
            print()
    
    if not output_to_stdout:
        print(f"Loading OpenAPI spec from {input_file}...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            spec = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON: {e}", file=sys.stderr)
        sys.exit(1)
    
    if not output_to_stdout:
        print(f"Loaded spec with {len(spec.get('components', {}).get('schemas', {}))} schemas")
        if args.filter_tags:
            print(f"Will filter to tags: {', '.join(args.filter_tags)}")
        print("\nNormalizing OpenAPI spec...")
    
    normalized_spec = normalize_openapi_spec(spec, custom_renames, 
                                            filter_tags=args.filter_tags,
                                            type_fixes=type_fixes if type_fixes else None,
                                            verbose=not output_to_stdout)
    
    # Write output
    if output_to_stdout:
        json.dump(normalized_spec, sys.stdout, indent=2)
        sys.stdout.write('\n')
    else:
        print(f"\nWriting normalized spec to {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(normalized_spec, f, indent=2)
        
        print(f"\n✓ Successfully created {output_file}")
        print(f"\nTo validate, run:")
        print(f"  openapi lint {output_file}")


if __name__ == '__main__':
    main()
