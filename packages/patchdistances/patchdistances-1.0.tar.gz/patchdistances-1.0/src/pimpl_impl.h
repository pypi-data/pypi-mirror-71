/*! \file pimpl_impl.h
	\brief Pimpl idiom; decoupling compilation units (implementation)
	\sa pimpl.h
*/

#pragma once

#include <memory>
#include <utility>

// Template class definition of 'pimpl.h'

template<typename T>
pimpl<T>::pimpl() : m{std::make_unique<T>()}
{
}

//! Perfect forwarding constructor.
template<typename T>
template<typename... Args>
pimpl<T>::pimpl(Args&&... args) : m{std::make_unique<T>(std::forward<Args>(args)...)}
{
}

template<typename T>
pimpl<T>::~pimpl() noexcept
{
}

template<typename T>
T* pimpl<T>::operator->() noexcept
{
	return m.get();
}

template<typename T>
const T* pimpl<T>::operator->() const noexcept
{
	return m.get();
}

template<typename T>
T& pimpl<T>::operator*() noexcept
{
	return *m.get();
}

template<typename T>
const T& pimpl<T>::operator*() const noexcept
{
	return *m.get();
}