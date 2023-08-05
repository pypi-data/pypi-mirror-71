/*! \file pimpl.h
	\brief Pimpl idiom; decoupling compilation units
*/

#pragma once

#include <memory>

//! Template class declaration for a pimpl implementation that decouples compilation units.
template<typename T>
class pimpl final
{
  private:
	std::unique_ptr<T> m;

  public:
	//! Default constructor.
	pimpl();
	//! Perfect forwarding constructor.
	template<typename... Args>
	pimpl(Args&&...);
	//! Destructor.
	~pimpl() noexcept;
	//! Access to implementation.
	T* operator->() noexcept;
	//! Const access to implementation.
	const T* operator->() const noexcept;
	//! Reference to implementation.
	T& operator*() noexcept;
	//! Const reference to implementation.
	const T& operator*() const noexcept;
};